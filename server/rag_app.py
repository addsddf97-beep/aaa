"""
RAG 터미널 테스트 UI

학생들이 터미널에서 직접 질문을 입력하고 답변을 확인할 수 있습니다.

사용법:
    python server/rag_app.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from rag_core import build_rag_engine


def print_separator():
    """구분선 출력"""
    print("\n" + "=" * 80 + "\n")


def print_answer(result: dict):
    """답변 및 출처를 보기 좋게 출력"""
    print_separator()
    print("💬 답변:")
    print(result['answer'])

    print("\n📚 출처:")
    if result['sources']:
        for idx, source in enumerate(result['sources'], 1):
            print(f"  [{idx}] {source['title']}")
            print(f"      {source['content_preview']}")
    else:
        print("  (출처 없음)")
    print_separator()


def main():
    """메인 실행 함수"""
    # 1. 환경 변수 로드
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        print("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일에 'GEMINI_API_KEY=your_key' 를 추가하세요.")
        sys.exit(1)

    # 2. projects.json 경로 찾기
    current_dir = Path(__file__).parent
    projects_json = current_dir.parent / "data" / "projects.json"

    if not projects_json.exists():
        print(f"❌ projects.json을 찾을 수 없습니다: {projects_json}")
        sys.exit(1)

    # 3. RAG 엔진 초기화
    print("🚀 RAG 엔진 초기화 중...")
    print(f"📁 프로젝트 데이터: {projects_json}")

    # 학생들이 여기서 파라미터 튜닝 가능
    rag_engine = build_rag_engine(
        projects_json_path=str(projects_json),
        gemini_api_key=gemini_api_key,
        rebuild=False,  # True로 바꾸면 벡터 DB 재구축
        top_k=2,  # 검색할 문서 개수 (학생 튜닝 포인트)
        chunk_size=1000,  # 청크 크기 (학생 튜닝 포인트)
        chunk_overlap=0  # 청크 겹침 (학생 튜닝 포인트)
    )

    print_separator()
    print("✅ RAG 시스템 준비 완료!")
    print("\n💡 사용법:")
    print("  - 질문을 입력하면 프로젝트 정보를 기반으로 답변합니다")
    print("  - 종료하려면 'exit', 'quit', '종료' 입력")
    print_separator()

    # 4. 대화 루프
    while True:
        # 질문 입력
        question = input("\n🤔 질문: ").strip()

        # 종료 명령 체크
        if question.lower() in ['exit', 'quit', '종료', 'q']:
            print("\n👋 종료합니다.")
            break

        # 빈 입력 무시
        if not question:
            continue

        # RAG 실행
        try:
            print("\n🔍 검색 중...")
            result = rag_engine.query(question)
            print_answer(result)

        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")
            print("   다시 시도해주세요.")


if __name__ == "__main__":
    main()
