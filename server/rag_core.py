"""
RAG 핵심 엔진: 검색 + 생성 + 출처 반환 (최종 싱크 버전)

학생들은 이 파일에서 다음을 튜닝할 수 있습니다:
- top_k (검색 개수)
- chunk_size (문서 분할 크기)
- 임베딩 모델 변경
- retriever 전략 변경
"""

import os
import json
from typing import List, Dict, Any
from pathlib import Path

# ChromaDB의 익명 telemetry는 posthog 버전 조합에 따라 경고를 낼 수 있습니다.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

try:
    from .prompts import BASELINE_SYSTEM_PROMPT, QA_PROMPT_TEMPLATE
except ImportError:
    from prompts import BASELINE_SYSTEM_PROMPT, QA_PROMPT_TEMPLATE


class RAGEngine:
    """
    프로젝트 포트폴리오를 위한 RAG 엔진

    주요 기능:
    1. projects.json 로드 및 벡터화
    2. 질문에 대한 유사 문서 검색
    3. LLM 기반 답변 생성 + 출처 반환
    """

    def __init__(
        self,
        projects_json_path: str,
        gemini_api_key: str,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db",
        top_k: int = 3,
        chunk_size: int = 1000,
        chunk_overlap: int = 0
    ):
        """
        Args:
            projects_json_path: projects.json 파일 경로
            gemini_api_key: Gemini API 키
            embedding_model: HuggingFace 임베딩 모델명 (학생 튜닝 가능)
            persist_directory: ChromaDB 저장 경로
            top_k: 검색할 문서 개수 (학생 튜닝 가능)
            chunk_size: 문서 분할 크기 (학생 튜닝 가능)
            chunk_overlap: 청크 간 겹침 (학생 튜닝 가능)
        """
        self.projects_json_path = projects_json_path
        self.gemini_api_key = gemini_api_key
        self.top_k = top_k
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.persist_directory = persist_directory

        # 1. 임베딩 모델 초기화 (무료)
        print(f"🔧 임베딩 모델 로딩: {embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},  # GPU 없어도 작동
            encode_kwargs={'normalize_embeddings': True}
        )

        # 2. LLM 초기화 (Gemini 2.5 Flash)
        print("🔧 LLM 초기화: Gemini 2.5 Flash")
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            google_api_key=gemini_api_key,
            temperature=0.3,
            max_output_tokens=700,
        )

        # 3. 벡터 스토어 초기화
        self.vectorstore = None
        self.qa_chain = None

    def _chroma_client_settings(self) -> Settings:
        """ChromaDB telemetry를 끈 클라이언트 설정."""
        return Settings(anonymized_telemetry=False)

    def load_projects(self) -> List[Document]:
        """
        [필드 동기화 완료]
        projects.json을 로드하여 LangChain Document 형식으로 변환합니다.
        웹 화면 모달창용 'detail' 필드와 RAG용 필드들을 모두 합쳐 AI에게 주입합니다.
        """
        with open(self.projects_json_path, 'r', encoding='utf-8') as f:
            projects = json.load(f)

        documents = []
        for idx, project in enumerate(projects):
            # 1. 원본 JSON 필드 안전하게 바인딩 (프로젝트 외의 모든 이력 타입 포괄 호환)
            title = project.get('title') or project.get('name') or f"project_{idx}"
            description = project.get('description', '')
            
            # 신규 보강된 상세 내역 및 역량 지표 로드
            detail = project.get('detail') or description
            role = project.get('role', 'N/A')
            result = project.get('result', 'N/A')
            
            tags_list = project.get('tags') or project.get('stack') or []
            link = project.get('link') or "N/A"
            period = project.get('period') or project.get('year') or "N/A"
            item_type = project.get('type', 'project')

            # 2. 모달 팝업 텍스트 깊이와 AI 검색 풀(Pool)의 지식 깊이를 1:1로 일치화
            content = f"""항목 유형: {item_type}
제목/이름: {title}
진행 기간: {period}
개요 설명: {description}
상세 수행 내용: {detail}
담당 역할 및 태스크: {role}
핵심 성과 및 결과 지표: {result}
사용 기술 및 태그: {', '.join(tags_list) if isinstance(tags_list, list) else tags_list}
링크: {link}"""

            # 3. 크로마 DB 매핑용 랭체인 문서 규격화 (출처 추적용 메타데이터 삽입)
            doc = Document(
                page_content=content,
                metadata={
                    'source': title,
                    'project_id': idx,
                    'tags': ', '.join(tags_list) if isinstance(tags_list, list) else tags_list
                }
            )
            documents.append(doc)

        print(f"✅ [RAG 동기화 가동] {len(documents)}개 항목의 상세 종합 컨텍스트 빌드 완료")
        return documents

    def build_vectorstore(self):
        """
        벡터 스토어 구축: 문서 로드 → 청킹 → 임베딩 → ChromaDB 저장
        """
        # 1. 프로젝트 로드
        documents = self.load_projects()

        # 2. 텍스트 분할 (학생이 chunk_size 튜닝 가능)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        splits = text_splitter.split_documents(documents)
        print(f"📄 {len(splits)}개 청크로 분할")

        # 3. 벡터 스토어 생성 (ChromaDB)
        print("💾 ChromaDB에 임베딩 저장 중...")
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            client_settings=self._chroma_client_settings()
        )
        print(f"✅ 벡터 스토어 구축 완료: {self.persist_directory}")

    def build_qa_chain(self):
        """
        QA Chain 구성: Retriever + LLM + Prompt
        """
        if self.vectorstore is None:
            raise ValueError("벡터 스토어가 없습니다. build_vectorstore()를 먼저 실행하세요.")

        # Retriever 설정 (top_k 개수만큼 검색)
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.top_k}
        )

        # 프롬프트 템플릿 설정
        prompt = PromptTemplate(
            template=BASELINE_SYSTEM_PROMPT + "\n\n" + QA_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )

        # RetrievalQA 체인 구성
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        print("✅ QA Chain 구축 완료")

    def query(self, question: str) -> Dict[str, Any]:
        """
        질문에 대한 답변 + 출처 반환 (출처 추적 완벽 보정 버전)

        Args:
            question: 사용자 질문

        Returns:
            {
                'answer': 답변 텍스트,
                'sources': [출처 정보 리스트]
            }
        """
        if self.qa_chain is None:
            raise ValueError("QA Chain이 없습니다. build_qa_chain()을 먼저 실행하세요.")

        # 1. 체인을 구동하여 AI 답변 생성
        result = self.qa_chain.invoke({"query": question})
        answer_text = result.get('result') or result.get('answer') or "답변을 생성하지 못했습니다."

        # 2. [보정] 체인 내부 출처가 유실되는 문제를 방지하기 위해 
        #    벡터 스토어에서 직접 유사 문서(Top_K)를 한 번 더 명확하게 조회합니다.
        sources = []
        try:
            # 질문과 가장 연관성 높은 원본 문서 조각들을 가져옵니다.
            matched_docs = self.vectorstore.similarity_search(question, k=self.top_k)
            
            for doc in matched_docs:
                # 우리가 JSON 파싱할 때 metadata['source']에 저장했던 프로젝트 타이틀 추출
                source_name = doc.metadata.get('source') or doc.metadata.get('name')
                
                # 중복되지 않게 리스트에 담아줍니다.
                if source_name and source_name not in sources:
                    sources.append(source_name)
        except Exception as e:
            print(f"⚠️ 출처 문서 역추적 중 경고 발생: {e}")

        # 3. 만약 체인 내부에서 우연히 꺼내진 소스가 있다면 백업으로 합쳐줍니다.
        for doc in result.get('source_documents', []):
            source_name = doc.metadata.get('source') or doc.metadata.get('name')
            if source_name and source_name not in sources:
                sources.append(source_name)

        # api.py의 ChatResponse 데이터 모델 규격에 맞춰 최종 리턴
        return {
            'answer': answer_text,
            'sources': sources
        }


    @classmethod
    def from_existing_db(
        cls,
        projects_json_path: str,
        gemini_api_key: str,
        persist_directory: str = "./chroma_db",
        **kwargs
    ):
        """
        이미 구축된 벡터 DB를 재사용 (재실행 시 빠름)
        """
        instance = cls(
            projects_json_path=projects_json_path,
            gemini_api_key=gemini_api_key,
            persist_directory=persist_directory,
            **kwargs
        )

        # 기존 DB 로드
        print(f"📂 기존 벡터 DB 로드: {persist_directory}")
        instance.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=instance.embeddings,
            client_settings=instance._chroma_client_settings()
        )
        instance.build_qa_chain()
        return instance


def build_rag_engine(
    projects_json_path: str,
    gemini_api_key: str,
    rebuild: bool = False,
    **kwargs
) -> RAGEngine:
    """
    RAG 엔진 빌더 (편의 함수)

    Args:
        projects_json_path: projects.json 경로
        gemini_api_key: Gemini API 키
        rebuild: True면 벡터 DB 재구축, False면 기존 DB 재사용
        **kwargs: RAGEngine 생성자 파라미터

    Returns:
        RAGEngine 인스턴스
    """
    persist_dir = kwargs.get('persist_directory', './chroma_db')

    # 기존 DB가 있고 rebuild=False면 재사용
    if not rebuild and os.path.exists(persist_dir):
        print("🔄 기존 벡터 DB 재사용")
        return RAGEngine.from_existing_db(
            projects_json_path=projects_json_path,
            gemini_api_key=gemini_api_key,
            **kwargs
        )

    # 새로 구축
    print("🏗️  벡터 DB 새로 구축")
    engine = RAGEngine(
        projects_json_path=projects_json_path,
        gemini_api_key=gemini_api_key,
        **kwargs
    )
    engine.build_vectorstore()
    engine.build_qa_chain()
    return engine
