"""
실습 2: 문서 분할

목표:
- 실습 1에서 만든 Document를 작은 chunk로 나눕니다.
- chunk_size를 바꿔 보며 조각 수 변화를 관찰합니다.
"""

import importlib.util
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


def _load_step01():
    path = Path(__file__).resolve().parent / "01_load_docs.py"
    spec = importlib.util.spec_from_file_location("step01_load_docs", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("01_load_docs.py를 불러올 수 없습니다.")
    spec.loader.exec_module(module)
    return module


def split_documents():
    # 실습 1 모듈로부터 전체 Document 리스트를 가져옵니다.
    docs = _load_step01().load_documents()

    # TODO: RecursiveCharacterTextSplitter를 만드세요.
    # 힌트: chunk_size=300, chunk_overlap=50
    # 줄바꿈(\n) 단위를 기본으로 끊어 문맥이 최대한 안 깨지도록 분할합니다.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    # TODO: splitter.split_documents(docs)를 호출하세요.
    chunks = splitter.split_documents(docs)

    return docs, chunks


if __name__ == "__main__":
    docs, chunks = split_documents()
    print("분할 전:", len(docs), "-> 분할 후:", len(chunks))
    
    # 분할된 결과물 샘플 확인을 위한 추가 코드
    if chunks:
        print("\n--- 첫 번째 분할 조각(Chunk 0) ---")
        print(chunks[0].page_content)
        print("Metadata:", chunks[0].metadata)
