# 문제 해결

## ModuleNotFoundError

가상환경이 꺼져 있을 가능성이 큽니다.

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## API key not valid

`.env` 파일의 `GEMINI_API_KEY` 값을 확인하세요.

```env
GEMINI_API_KEY=your_key_here
```

## 같은 프로젝트가 여러 번 나옴

인덱스를 여러 번 만들며 중복 저장되었을 수 있습니다.

```bash
rm -rf lessons/rag-handout/chroma_db
python lessons/rag-handout/03_build_index.py
```

## 답변이 이상함

먼저 검색 결과를 확인합니다.

```bash
python lessons/rag-handout/04_search_test.py
```

