# AI Portfolio RAG Chatbot Template

AI 기반 포트폴리오 웹사이트 + RAG 챗봇 실습 템플릿

---

## 🎯 프로젝트 소개

자신의 프로젝트를 구조화된 데이터로 문서화하고, 개성 있는 포트폴리오 웹사이트를 만든 뒤,
**나에 대해 질문하면 출처와 함께 답변하는 RAG 챗봇**을 얹어 배포까지 완성합니다.

### 최종 산출물
- ✅ `data/projects.json` - 검색 가능한 프로젝트 데이터
- ✅ 개인 포트폴리오 웹사이트 (GitHub Pages)
- ✅ RAG 기반 챗봇 API (Render)
- ✅ 출처 인용 답변 시스템

---

## 📚 수업 로드맵

실습은 다음 순서로 진행됩니다:

| 단계 | 내용 | 문서 | 예상 시간 |
|:---:|------|------|:---:|
| **0** | 전체 개요 및 아키텍처 이해 | [docs/00-OVERVIEW.md](docs/00-OVERVIEW.md) | 
| **1** | 프로젝트 데이터 구축 | [docs/01-DATA.md](docs/01-DATA.md) | 
| **2** | 포트폴리오 웹앱 제작 | [docs/02-WEBAPP.md](docs/02-WEBAPP.md) | 
| **3** | RAG 챗봇 구축 및 튜닝 | [docs/03-RAG.md](docs/03-RAG.md) | 
| **4** | 배포 및 연동 | [docs/04-DEPLOY.md](docs/04-DEPLOY.md) | 

### 참고 문서
- [SPEC-ARCHITECTURE.md](docs/SPEC-ARCHITECTURE.md) - 전체 아키텍처 명세
- [SPEC-BACKEND.md](docs/SPEC-BACKEND.md) - 백엔드 흐름 명세
- [REFERENCES.md](docs/REFERENCES.md) - 포트폴리오 사이트 참고 자료

---

## 🚀 빠른 시작

### 1️⃣ 템플릿으로 저장소 생성

GitHub에서 **"Use this template"** 버튼 클릭 → 본인 저장소 생성

### 2️⃣ 로컬에 클론

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 3️⃣ 환경 설정

```bash
# Python 가상환경 생성 (환경에 맞게 선택)
python3 -m venv .venv      # macOS/Linux
# 또는
python -m venv .venv       # Windows (대부분)
# 또는
py -m venv .venv          # Windows (Microsoft Store 설치)

# 가상환경 활성화
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate     # Windows CMD
# 또는
.venv\Scripts\Activate.ps1 # Windows PowerShell

# 의존성 설치
pip install -r requirements.txt

# API 키 설정
cp .env.example .env       # macOS/Linux
# 또는
copy .env.example .env     # Windows
# .env 파일을 열어 GEMINI_API_KEY 입력
```

**Gemini API 키 발급:**
- https://aistudio.google.com/apikey 접속
- "Create API Key" 클릭
- 발급된 키를 `.env` 파일에 붙여넣기

### 4️⃣ 프로젝트 데이터 빌드

```bash
# 예시 프로젝트 확인
ls data/projects/

# projects.json 생성
python3 data/build.py
```

출력:
```
📂 2개의 프로젝트 폴더를 발견했습니다.

✅ interlocutor-adaptation: Interlocutor Adaptation Dialogue System
✅ persona-scheduling: Dynamic Persona Scheduling Framework

🎉 성공! projects.json 파일이 생성되었습니다.
   총 2개의 프로젝트가 포함되었습니다.
```

### 5️⃣ 단계별 실습 시작

[docs/00-OVERVIEW.md](docs/00-OVERVIEW.md)부터 순서대로 진행하세요!

---

## 📁 프로젝트 구조

```
ai-portfolio-template/
├── README.md                    # 👈 지금 보고 있는 파일
├── .env.example                 # API 키 설정 예시
├── .gitignore
├── requirements.txt
│
├── 📂 docs/                     # 📚 학습 문서
│   ├── 00-OVERVIEW.md          # 전체 개요
│   ├── 01-DATA.md              # 데이터 구축
│   ├── 02-WEBAPP.md            # 웹앱 제작
│   ├── 03-RAG.md               # RAG 챗봇
│   ├── 04-DEPLOY.md            # 배포
│   ├── SPEC-ARCHITECTURE.md    # 아키텍처 명세
│   ├── SPEC-BACKEND.md         # 백엔드 명세
│   └── REFERENCES.md           # 참고 자료
│
├── 📂 data/
│   ├── 📂 projects/             # 📁 프로젝트 폴더 (각 프로젝트별 관리)
│   │   ├── project-1/
│   │   │   ├── project.json    # 프로젝트 메타데이터
│   │   │   └── README.md       # 상세 설명 (선택)
│   │   └── project-2/
│   ├── build.py                 # 빌드 스크립트
│   └── projects.json            # ⭐ 통합 데이터 (빌드 결과)
│
├── 📂 web/                      # 🌐 포트폴리오 웹사이트
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── widget.js               # 챗봇 위젯
│
├── 📂 server/                   # 🤖 RAG 백엔드
│   ├── rag_core.py             # RAG 엔진
│   ├── rag_app.py              # 로컬 테스트 UI
│   ├── prompts.py              # 프롬프트 모음
│   └── api.py                  # FastAPI 서버
│
└── 📂 .github/workflows/
    └── deploy.yml              # 자동 배포 설정
```

---

## 🛠️ 기술 스택

### 프론트엔드
- **HTML / CSS / JavaScript** (Vanilla)
- **GitHub Pages** (배포)

### 백엔드
- **Python** 3.9+
- **FastAPI** - API 서버
- **LangChain** - RAG 파이프라인
- **ChromaDB** - 벡터 데이터베이스
- **Gemini Flash** - LLM (무료)
- **Render** - 백엔드 배포 (무료)

---

## 💡 핵심 기능

### 1. 프로젝트 데이터 구조화
- 각 프로젝트를 폴더로 관리 (`data/projects/프로젝트명/`)
- `project.json`으로 메타데이터 작성
- `build.py`로 통합 (`data/projects.json`)

### 2. 동적 포트폴리오 웹사이트
- `projects.json`을 읽어 프로젝트 카드 자동 렌더링
- 개성 있는 디자인 커스터마이징
- 반응형 레이아웃

### 3. RAG 기반 챗봇
- 프로젝트 데이터 기반 질의응답
- 출처(sources) 함께 반환
- 근거 없는 질문에는 "모른다"고 답변

### 4. 무료 배포
- GitHub Pages (프론트엔드)
- Render (백엔드 API)
- 도메인 연결 가능

---


## 🐛 문제 해결

### 환경 설정 오류

```bash
# Python 버전 확인
python3 --version

# pip 업그레이드
pip install --upgrade pip

# 가상환경 다시 생성
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Gemini API 오류

- **401 Unauthorized**: API 키가 잘못됨 → `.env` 파일 확인
- **429 Too Many Requests**: 무료 티어 제한 (15 RPM) → 1분 대기

