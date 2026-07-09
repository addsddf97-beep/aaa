"""
실습 3: 벡터 인덱스 구축
"""

import importlib.util
import os
import shutil
import warnings
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma

warnings.filterwarnings("ignore", category=FutureWarning)

from langchain_google_genai import GoogleGenerativeAIEmbeddings


CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


def _load_step02():
    path = Path(__file__).resolve().parent / "02_split_docs.py"
    spec = importlib.util.spec_from_file_location("step02_split_docs", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("02_split_docs.py를 불러올 수 없습니다.")
    spec.loader.exec_module(module)
    return module


def build_index(rebuild: bool = True):
    load_dotenv()

    _, chunks = _load_step02().split_documents()

    if rebuild and CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(".env 파일에 GEMINI_API_KEY를 설정하세요.")

    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )
    db = Chroma.from_documents(
        documents=chunks,
        embedding=emb,
        persist_directory=str(CHROMA_DIR),
    )

    return db


if __name__ == "__main__":
    db = build_index()
    print("저장된 조각:", db._collection.count())