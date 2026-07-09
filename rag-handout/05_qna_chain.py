"""
실습 5: QnA 체인 완성
"""

import os
import warnings
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

warnings.filterwarnings("ignore", category=FutureWarning)

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


def create_chain():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(".env 파일에 GEMINI_API_KEY를 설정하세요.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
    )
    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )
    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=emb,
    )
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # 프롬프트를 면접/포트폴리오 분석 스타일로 고도화했습니다.
    prompt = ChatPromptTemplate.from_template(
        """
너는 지원자의 프로젝트 포트폴리오를 매력적으로 소개하는 전문 AI 커리어 어시스턴트야.
반드시 아래 제공된 [문서] 내용만을 철저한 근거로 삼아 답변을 작성해야 해.

[답변 원칙]
1. 질문에 가장 알맞은 프로젝트의 '이름', '개요', '역할', '성과'를 빠짐없이 요약하여 답변해줘.
2. 어조는 비즈니스에 적합하도록 정중하고 신뢰감 있는 문체(~습니다, ~입니다)를 사용해줘.
3. 만약 제공된 [문서]에 질문과 관련된 프로젝트나 정보가 전혀 없다면, 상상해서 지어내지 말고 정확히 "포트폴리오에 없는 정보입니다."라고 답변해야 해.

[문서]
{context}

[질문]
{question}

[답변]:
"""
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


chain = create_chain()


if __name__ == "__main__":
    # 1. 학교 생활 문제를 해결한 프로젝트 테스트
    print("=== 질문 1 ===")
    print(chain.invoke("학교 생활의 문제를 해결하려고 만든 서비스는?"))
    
    # 2. 포트폴리오에 없는 엉뚱한 내용 테스트 (예외 처리 확인용)
    print("\n=== 질문 2 ===")
    print(chain.invoke("블록체인이나 NFT 관련 프로젝트 경험이 있나요?"))
