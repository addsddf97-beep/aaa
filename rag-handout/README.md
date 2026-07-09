# RAG 실습 핸드아웃 - 학생용

이 폴더는 수업 중 직접 코드를 채워 넣는 버전입니다.

## 실행 순서

프로젝트 루트에서 가상환경을 켠 뒤 진행합니다.

```bash
source .venv/bin/activate
```

Windows PowerShell에서는 다음을 사용합니다.

```powershell
.venv\Scripts\Activate.ps1
```

API 키는 프로젝트 루트의 `.env` 파일에 저장합니다.

```env
GEMINI_API_KEY=your_key_here
```

실습 순서:

```bash
python lessons/rag-handout/00_hello_llm.py
python lessons/rag-handout/01_load_docs.py
python lessons/rag-handout/02_split_docs.py
python lessons/rag-handout/03_build_index.py
python lessons/rag-handout/04_search_test.py
python lessons/rag-handout/05_qna_chain.py
python lessons/rag-handout/06_chat.py
python lessons/rag-handout/07_eval/evaluate.py
```

프로젝트 예시 데이터는 이 폴더의 `projects.sample.json`을 사용합니다.

예시 질문은 `QUESTIONS.md`에 있습니다.

튜닝 결과 평가는 `07_eval/` 폴더에서 진행합니다. 평가셋과 평가 기준은 `07_eval/eval_dataset.json`, `07_eval/EVALUATION_GUIDE.md`를 확인하세요.

