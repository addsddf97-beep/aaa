"""
실습 6: 터미널 챗봇
"""

import importlib.util
from pathlib import Path


def _load_step05():
    path = Path(__file__).resolve().parent / "05_qna_chain.py"
    spec = importlib.util.spec_from_file_location("step05_qna_chain", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("05_qna_chain.py를 불러올 수 없습니다.")
    spec.loader.exec_module(module)
    return module


chain = _load_step05().chain

print("포트폴리오 챗봇입니다. exit 입력 시 종료.")

while True:
    q = input("\n질문 > ").strip()

    if q in ("exit", "quit"):
        break

    if not q:
        continue

    print(chain.invoke(q))
