# Step 3: RAG 챗봇 구축

`data/projects.json`에 있는 프로젝트 정보를 바탕으로 질문에 답하는 챗봇을 만듭니다.

---

## 목표

이 단계에서 해야 할 일은 세 가지입니다.

1. `projects.json`을 RAG 검색 데이터로 사용하기
2. 터미널에서 RAG 챗봇 테스트하기
3. 웹앱 오른쪽 아래 챗봇 위젯과 RAG API 연결하기

---

## 1. 준비

프로젝트 루트 폴더에서 실행합니다.

```bash
cd /path/to/gbsw-ai-portfolio-template
```

가상환경을 활성화합니다.

```bash
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

Gemini API 키가 있는지 확인합니다.

```bash
cat .env
```

`.env` 파일에는 다음 값이 있어야 합니다.

```env
GEMINI_API_KEY=your_key_here
```

API 키는 Google AI Studio에서 발급합니다.

```text
https://aistudio.google.com/apikey
```

프로젝트 데이터를 최신 상태로 만듭니다.

```bash
python data/build.py
```

---

## 2. 터미널에서 먼저 테스트

먼저 웹앱 연결 전에 RAG 자체가 잘 동작하는지 확인합니다.

```bash
python server/rag_app.py
```

첫 실행은 임베딩 모델 다운로드와 ChromaDB 생성 때문에 1~2분 정도 걸릴 수 있습니다.

정상 실행 예시:

```text
🚀 RAG 엔진 초기화 중...
✅ 2개 프로젝트 로드 완료
📄 2개 청크로 분할
💾 ChromaDB에 임베딩 저장 중...
✅ 벡터 스토어 구축 완료: ./chroma_db
✅ QA Chain 구축 완료
✅ RAG 시스템 준비 완료!
```

질문 예시:

```text
어떤 프로젝트를 했나요?
```

정상이라면 프로젝트 제목과 출처가 함께 나옵니다.

종료하려면 다음 중 하나를 입력합니다.

```text
exit
quit
종료
```

---

## 3. 웹앱에서 RAG 챗봇 보기

웹앱에서 챗봇을 보려면 서버를 두 개 실행해야 합니다.

- 터미널 1: RAG API 서버
- 터미널 2: 웹 서버

### 터미널 1: RAG API 서버 실행

프로젝트 루트에서 실행합니다.

```bash
source .venv/bin/activate
python data/build.py
python -m uvicorn server.api:app --host 127.0.0.1 --port 8000
```

성공하면 다음과 비슷하게 보입니다.

```text
✅ RAG 엔진 준비 완료!
Uvicorn running on http://127.0.0.1:8000
```

API 서버가 정상인지 확인합니다.

```bash
curl http://127.0.0.1:8000/health
```

정상 응답:

```json
{"status":"healthy","rag_engine":"ready"}
```

질문 API만 직접 테스트할 수도 있습니다.

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "어떤 프로젝트를 했나요?"}'
```

### 터미널 2: 웹 서버 실행

API 서버는 끄지 말고, 새 터미널을 엽니다.

```bash
cd /path/to/gbsw-ai-portfolio-template/web
python3 -m http.server 4173
```

브라우저에서 접속합니다.

```text
http://127.0.0.1:4173
```

오른쪽 아래 챗봇에 질문을 입력합니다.

```text
어떤 프로젝트를 했나요?
```

---

## 4. 연결 구조

웹 챗봇은 `web/widget.js`에서 API 서버로 질문을 보냅니다.

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

전체 흐름은 다음과 같습니다.

```text
브라우저
  ↓
web/index.html + web/widget.js
  ↓ fetch()
server/api.py의 POST /chat
  ↓
server/rag_core.py
  ↓
data/projects.json + chroma_db/
```

즉, 프로젝트 내용을 바꾸려면 먼저 `data/projects/각프로젝트/project.json`을 수정하고 `python data/build.py`를 다시 실행합니다.

---

## 5. RAG 원리 한눈에 보기

일반 LLM은 내 프로젝트 데이터를 모릅니다.

```text
질문: 어떤 프로젝트를 했나요?
일반 LLM: 알 수 없습니다. 또는 추측합니다.
```

RAG는 먼저 내 데이터를 검색한 뒤, 검색 결과를 LLM에게 함께 줍니다.

```text
질문
  ↓
질문을 임베딩 벡터로 변환
  ↓
ChromaDB에서 비슷한 프로젝트 검색
  ↓
검색된 프로젝트 내용을 Gemini에게 전달
  ↓
근거 기반 답변 생성
```

이 프로젝트에서는 다음 파일들이 핵심입니다.

```text
data/projects.json     # 프로젝트 데이터
chroma_db/             # 임베딩 저장소
server/rag_core.py     # RAG 엔진
server/rag_app.py      # 터미널 테스트
server/api.py          # 웹 챗봇 API
web/widget.js          # 웹 챗봇 UI
```

---

## 6. 학생이 수정해볼 곳

처음에는 많이 바꾸지 말고 아래 두 가지만 실험합니다.

### 검색 개수 바꾸기

[server/rag_app.py](../server/rag_app.py) 또는 [server/api.py](../server/api.py)에서 `top_k`를 조정합니다.

```python
top_k=2
```

권장값:

```text
프로젝트 2~3개: top_k=2
프로젝트 5개 이상: top_k=3
```

### 답변 스타일 바꾸기

[server/prompts.py](../server/prompts.py)의 프롬프트를 수정합니다.

예시:

```python
BASELINE_SYSTEM_PROMPT = """
당신은 AI 포트폴리오 질의응답 도우미입니다.
제공된 프로젝트 문서에 있는 내용만 근거로 답변하세요.
모르는 내용은 추측하지 말고 모른다고 답하세요.
답변은 한국어로 간결하게 작성하세요.
"""
```

수정 후에는 서버를 껐다가 다시 실행합니다.

---

## 7. 문제 해결

### GEMINI_API_KEY가 설정되지 않았습니다

`.env` 파일이 없거나 API 키가 비어 있는 상태입니다.

```bash
cp .env.example .env
```

`.env` 파일을 열어 값을 입력합니다.

```env
GEMINI_API_KEY=AIzaSy...
```

### projects.json을 찾을 수 없습니다

프로젝트 루트에서 다음 명령을 실행합니다.

```bash
python data/build.py
ls data/projects.json
```

### 웹 챗봇이 서버 오류를 보여줍니다

먼저 API 서버가 켜져 있는지 확인합니다.

```bash
curl http://127.0.0.1:8000/health
```

안 되면 터미널 1에서 다시 실행합니다.

```bash
source .venv/bin/activate
python -m uvicorn server.api:app --host 127.0.0.1 --port 8000
```

그다음 `web/widget.js`의 주소를 확인합니다.

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### ChromaDB 오류 또는 답변이 예전 데이터 기준으로 나옵니다

벡터 DB를 지우고 다시 만듭니다.

```bash
rm -rf chroma_db/
python server/rag_app.py
```

### ChromaDB telemetry 경고가 보입니다

다음 경고는 보통 실행을 막는 오류가 아닙니다.

```text
Failed to send telemetry event ...
```

계속 신경 쓰이면 의존성을 다시 설치합니다.

```bash
pip install -r requirements.txt
```

### Gemini API 429 오류

무료 사용량 제한에 걸린 경우입니다. 1~2분 기다린 뒤 다시 질문합니다.

---

## 8. 체크리스트

- [ ] `.env`에 `GEMINI_API_KEY`를 넣었다.
- [ ] `python data/build.py`를 실행했다.
- [ ] `python server/rag_app.py`에서 질문 테스트를 했다.
- [ ] `http://127.0.0.1:8000/health`가 정상이다.
- [ ] `http://127.0.0.1:4173`에서 웹 챗봇이 보인다.
- [ ] 웹 챗봇에서 `어떤 프로젝트를 했나요?` 질문에 답변이 나온다.

---

## 다음 단계

로컬에서 챗봇이 잘 동작하면 [Step 4: 배포](04-DEPLOY.md)로 넘어가 Render와 GitHub Pages에 배포합니다.
