"""
실습 7: RAG 평가 파이프라인

학생용 TODO 버전입니다.

학생이 해야 할 일:
- 코드 전체를 새로 작성하지 않습니다.
- # TODO 학생 작성 표시가 있는 줄의 ____ 부분만 채웁니다.
- 나머지 코드는 수정하지 않아도 됩니다.
"""

import argparse
import json
import os
import re
import warnings
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

warnings.filterwarnings("ignore", category=FutureWarning)

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


EVAL_DIR = Path(__file__).resolve().parent
LESSON_DIR = EVAL_DIR.parent
DATASET_PATH = EVAL_DIR / "eval_dataset.json"
RESULTS_PATH = EVAL_DIR / "eval_results.jsonl"
CHROMA_DIR = LESSON_DIR / "chroma_db"

ABSTAIN_PHRASES = [
    "포트폴리오에 없는 정보",
    "제공된",
    "찾을 수 없습니다",
    "알 수 없습니다",
]

SECTION_LINE = "=" * 80
SUB_LINE = "-" * 80


def load_dataset(path: Path) -> list[dict]:
    """
    eval_dataset.json 파일을 읽어서 list[dict]로 반환합니다.

    힌트:
    - json.load(f)를 사용합니다.
    """

    with open(path, encoding="utf-8") as f:
        # TODO 학생 작성: JSON 파일을 파이썬 객체로 읽어오세요. -> 정답: load
        return json.load(f)


def preprocess_query(text: str) -> str:
    """
    검색어의 여러 공백을 하나로 줄이고, 앞뒤 공백을 제거합니다.

    예:
    "  RAG    평가   파이프라인  "
    -> "RAG 평가 파이프라인"

    힌트:
    - strip()을 사용합니다.
    """

    text = re.sub(r"\s+", " ", text)

    # TODO 학생 작성: 앞뒤 공백을 제거하세요. -> 정답: strip
    text = text.strip()

    return text


def build_queries(item: dict) -> list[str]:
    """
    원 질문과 query_variants를 합쳐 검색어 리스트를 만듭니다.
    중복 검색어는 제거합니다.
    """

    raw_queries = [item["question"], *item.get("query_variants", [])]

    queries = []
    seen = set()

    for query in raw_queries:
        cleaned = preprocess_query(query)
        key = cleaned.casefold()

        if cleaned and key not in seen:
            queries.append(cleaned)

            # TODO 학생 작성: seen 집합에 key를 추가하세요. -> 정답: add
            seen.add(key)

    return queries


def create_llm_and_db():
    """
    Gemini LLM과 Chroma DB를 준비합니다.
    이 함수는 수정하지 않습니다.
    """

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(".env 파일에 GEMINI_API_KEY를 설정하세요.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2,
    )

    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )

    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=emb,
    )

    return llm, db


def retrieve_multi_query(db, queries: list[str], k: int) -> list:
    """
    여러 검색어로 Chroma DB를 검색합니다.
    프로젝트명 기준으로 중복 문서를 제거합니다.

    힌트:
    - docs_by_source는 딕셔너리입니다.
    - setdefault(source, doc)을 사용하면 같은 source가 이미 있을 때 덮어쓰지 않습니다.
    """

    docs_by_source = {}

    for query in queries:
        docs = db.similarity_search(query, k=k)

        for doc in docs:
            source = doc.metadata.get("name", "Unknown")

            # TODO 학생 작성: source를 key로 하여 doc을 저장하세요. -> 정답: setdefault
            docs_by_source.setdefault(source, doc)

    return list(docs_by_source.values())


def format_docs(docs) -> str:
    """
    검색된 Document 리스트를 LLM에 넣을 context 문자열로 합칩니다.

    힌트:
    - 각 문서의 본문은 doc.page_content입니다.
    """

    # TODO 학생 작성: doc의 본문 내용을 "\n\n"으로 이어 붙이세요. -> 정답: page_content
    return "\n\n".join(doc.page_content for doc in docs)


def generate_answer(llm, question: str, docs) -> str:
    """
    검색 문서를 근거로 LLM 답변을 생성합니다.
    """

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
"""
    )

    context = format_docs(docs)
    message = prompt.format_messages(context=context, question=question)

    # TODO 학생 작성: llm을 실행하세요. -> 정답: invoke
    response = llm.invoke(message)

    # TODO 학생 작성: LLM 응답의 문자열 내용만 반환하세요. -> 정답: content
    return response.content


def evaluate_sources(found_sources: list[str], expected_sources: list[str]) -> dict:
    """
    기대한 출처가 검색 결과에 모두 포함됐는지 평가합니다.
    """

    missing = [
        source
        for source in expected_sources
        if source not in found_sources
    ]

    if not expected_sources:
        coverage = 1.0
    else:
        coverage = (len(expected_sources) - len(missing)) / len(expected_sources)

    return {
        # TODO 학생 작성: missing이 비어 있으면 True가 되도록 작성하세요. -> 정답: 0
        "source_pass": len(missing) == 0,
        "missing_sources": missing,
        "source_coverage": coverage,
    }


def evaluate_answer(answer: str, expected_keywords: list[str], should_abstain: bool) -> dict:
    """
    답변에 기대 키워드가 있는지, 보류 응답을 했는지 평가합니다.

    이 함수는 난이도를 낮추기 위해 대부분 완성되어 있습니다.
    학생은 수정하지 않아도 됩니다.
    """

    missing_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword not in answer
    ]

    abstained = any(
        phrase in answer
        for phrase in ABSTAIN_PHRASES
    )

    if should_abstain:
        answer_pass = abstained and len(missing_keywords) == 0
    else:
        answer_pass = len(missing_keywords) == 0 and not abstained

    return {
        "answer_pass": answer_pass,
        "missing_keywords": missing_keywords,
        "abstained": abstained,
    }


def format_list(values: list[str]) -> str:
    """
    리스트를 출력용 문자열로 변환합니다.
    """

    return ", ".join(values) if values else "(없음)"


def pass_label(value: bool) -> str:
    """
    True/False를 PASS/FAIL로 변환합니다.
    """

    return "PASS" if value else "FAIL"


def ask_human_judgement(item: dict, answer: str) -> bool:
    """
    사람이 직접 모델 응답을 보고 y/n으로 평가합니다.
    """

    print("\n" + SUB_LINE)
    print("[사람 평가 입력]")
    print("아래 기준과 모델 응답을 비교해서, 이 문항의 의도한 행동을 했으면 y를 입력합니다.")

    print("\n[질문]")
    print(item["question"])

    print("\n[정답/의도 기준]")
    print("- 난이도:", item.get("difficulty", "unknown"))
    print("- 의도:", item["intended_behavior"])
    print("- 기대 출처:", format_list(item["expected_sources"]))
    print("- 기대 키워드:", format_list(item["expected_keywords"]))
    print("- 보류 응답 필요:", "예" if item["should_abstain"] else "아니오")

    print("\n[모델 응답]")
    print(answer)

    while True:
        value = input("의도한 행동을 했나요? (y/n): ").strip().lower()

        if value in ("y", "yes"):
            # TODO 학생 작성: y이면 True를 반환하세요. -> 정답: True
            return True

        if value in ("n", "no"):
            # TODO 학생 작성: n이면 False를 반환하세요. -> 정답: False
            return False

        print("y 또는 n으로 입력하세요.")


def save_result(result: dict):
    """
    평가 결과를 eval_results.jsonl 파일에 저장합니다.
    """

    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")


def print_case_result(result: dict):
    """
    문항 하나의 평가 결과를 화면에 출력합니다.
    이 함수는 수정하지 않습니다.
    """

    print("\n" + SECTION_LINE)
    print(f"[문항] {result['id']}")

    print("\n[질문]")
    print(result["question"])

    print("\n[정답/의도 기준]")
    print("- 난이도:", result.get("difficulty", "unknown"))
    print("- 의도:", result["intended_behavior"])
    print("- 기대 출처:", format_list(result["expected_sources"]))
    print("- 기대 키워드:", format_list(result["expected_keywords"]))
    print("- 보류 응답 필요:", "예" if result["should_abstain"] else "아니오")

    print("\n[검색 결과]")
    print("- 멀티 쿼리:", format_list(result["queries"]))
    print("- 검색된 출처:", format_list(result["found_sources"]))

    print("\n[모델 응답]")
    print(result["answer"])

    print("\n[평가 결과]")
    print("- 출처 평가:", pass_label(result["source_pass"]), f"(coverage={result['source_coverage']:.2f})")
    print("- 답변 평가:", pass_label(result["answer_pass"]))
    print("- 보류 응답 감지:", "예" if result["abstained"] else "아니오")
    print("- 자동 평가:", pass_label(result["auto_pass"]))
    print("- 사람 평가:", pass_label(result["human_pass"]) if result["human_evaluated"] else "SKIP")

    if result["missing_sources"] or result["missing_keywords"]:
        print("\n[누락 항목]")

        if result["missing_sources"]:
            print("- 누락 출처:", format_list(result["missing_sources"]))

        if result["missing_keywords"]:
            print("- 누락 키워드:", format_list(result["missing_keywords"]))


def main():
    """
    전체 평가 루프입니다.

    학생이 해야 할 일:
    - 아래 TODO 부분의 함수 호출만 채우면 됩니다.
    """

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--no-human", action="store_true")
    args = parser.parse_args()

    # TODO 학생 작성: 평가셋을 불러오세요. -> 정답: load_dataset
    dataset = load_dataset(DATASET_PATH)

    # TODO 학생 작성: LLM과 DB를 생성하세요. -> 정답: create_llm_and_db
    llm, db = create_llm_and_db()

    if RESULTS_PATH.exists():
        RESULTS_PATH.unlink()

    results = []

    for item in dataset:
        # TODO 학생 작성: 검색어 리스트를 만드세요. -> 정답: build_queries
        queries = build_queries(item)

        # TODO 학생 작성: 여러 검색어로 문서를 검색하세요. -> 정답: retrieve_multi_query
        docs = retrieve_multi_query(db, queries, k=args.k)

        found_sources = [
            doc.metadata.get("name", "Unknown")
            for doc in docs
        ]

        # TODO 학생 작성: LLM 답변을 생성하세요. -> 정답: generate_answer
        answer = generate_answer(llm, item["question"], docs)

        # TODO 학생 작성: 검색 출처를 평가하세요. -> 정답: evaluate_sources
        source_eval = evaluate_sources(
            found_sources,
            item["expected_sources"],
        )

        # TODO 학생 작성: 답변을 평가하세요. -> 정답: evaluate_answer
        answer_eval = evaluate_answer(
            answer,
            item["expected_keywords"],
            item["should_abstain"],
        )

        auto_pass = source_eval["source_pass"] and answer_eval["answer_pass"]

        human_evaluated = not args.no_human
        human_pass = True

        if not args.no_human:
            # TODO 학생 작성: 사람 평가 함수를 호출하세요. -> 정답: ask_human_judgement
            human_pass = ask_human_judgement(item, answer)

        result = {
            "id": item["id"],
            "question": item["question"],
            "difficulty": item.get("difficulty", "unknown"),
            "queries": queries,
            "found_sources": found_sources,
            "expected_sources": item["expected_sources"],
            "expected_keywords": item["expected_keywords"],
            "should_abstain": item["should_abstain"],
            "intended_behavior": item["intended_behavior"],
            "answer": answer,
            "auto_pass": auto_pass,
            "human_evaluated": human_evaluated,
            "human_pass": human_pass,
            **source_eval,
            **answer_eval,
        }

        results.append(result)
        save_result(result)
        print_case_result(result)

    auto_pass_count = sum(
        1 for result in results
        if result["auto_pass"]
    )

    human_pass_count = sum(
        1 for result in results
        if result["human_pass"]
    )

    complete_count = sum(
        1 for result in results
        if result["auto_pass"] and result["human_pass"]
    )

    print("\n" + SECTION_LINE)
    print("평가 요약")
    print(f"자동 평가 PASS: {auto_pass_count}/{len(results)}")
    print(f"사람 평가 PASS: {human_pass_count}/{len(results)}")
    print(f"완료 기준 PASS: {complete_count}/{len(results)}")
    print("결과 파일:", RESULTS_PATH)

    if complete_count == len(results):
        print("실습 7 완료: 모든 문항이 기준을 만족했습니다.")
    else:
        print("튜닝 필요: FAIL 문항의 검색 출처, 키워드, 보류 응답을 확인하세요.")


if __name__ == "__main__":
    main()
