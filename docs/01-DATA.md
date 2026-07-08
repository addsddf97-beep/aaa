# Step 1: 프로젝트 데이터 구축

검색 가능한 프로젝트 데이터 만들기

---

## 🎯 학습 목표

- 구조화된 데이터의 중요성 이해
- JSON 형식으로 프로젝트 정보 작성
- 검색을 위한 메타데이터 설계
- `data/projects.json` 완성

---

## 📊 왜 데이터부터 시작하는가?

```
data/projects/ (프로젝트 폴더)
    ├─→ project-1/
    │   └─→ project.json (메타데이터)
    ├─→ project-2/
    │   └─→ project.json
    └─→ ...
         ↓ build.py
data/projects.json (Single Source of Truth)
    ├─→ 웹사이트 (프로젝트 카드 렌더링)
    └─→ RAG 챗봇 (질의응답 검색)
```

**하나의 데이터 소스**를 만들면:
- ✅ 웹사이트와 챗봇이 같은 정보 사용
- ✅ 데이터 수정 시 한 곳만 변경
- ✅ 일관성 보장
- ✅ 각 프로젝트를 폴더로 관리하여 확장 가능

---

## 📝 projects.json 구조

### 기본 형식

```json
[
  {
    "id": "프로젝트 고유 식별자",
    "title": "프로젝트 제목",
    "description": "프로젝트 상세 설명 (검색 대상)",
    "tags": ["태그1", "태그2", "태그3"],
    "link": "GitHub 또는 프로젝트 링크"
  }
]
```

### 필수 필드

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| `id` | string | 고유 식별자 (영문, 하이픈 사용) | `"rag-chatbot"` |
| `title` | string | 프로젝트 제목 | `"RAG 기반 챗봇"` |
| `description` | string | 상세 설명 (RAG 검색 대상) | `"ChromaDB와 Gemini를 활용한..."` |
| `tags` | array | 기술/분야 태그 | `["Python", "LLM", "RAG"]` |
| `link` | string | 관련 링크 | `"https://github.com/..."` |

### 선택 필드 (확장 가능)

추가로 넣고 싶은 정보:

```json
{
  "id": "project-id",
  "title": "프로젝트 제목",
  "description": "상세 설명",
  "tags": ["Python", "AI"],
  "link": "https://...",

  "date": "2024-03",
  "duration": "3개월",
  "role": "백엔드 개발",
  "team": "4명",
  "tech_stack": ["FastAPI", "PostgreSQL"],
  "achievements": ["성능 30% 개선", "사용자 1000명 달성"],
  "image": "path/to/image.png"
}
```

---

## 🛠️ 실습: 프로젝트 데이터 작성하기

### 작업 방식

이 템플릿에서는 **프로젝트 폴더 기반** 구조를 사용합니다:

1. `data/projects/` 안에 각 프로젝트를 **별도 폴더**로 생성
2. 각 폴더에 `project.json` 작성
3. `python3 data/build.py` 실행하여 `projects.json` 자동 생성

### Step 1: 예시 프로젝트 확인

기본 예시가 이미 있습니다:

```bash
# 프로젝트 폴더 확인
ls data/projects/

# 예시 프로젝트 구조 확인
cat data/projects/interlocutor-adaptation/project.json
```

### Step 2: 프로젝트 선정

포트폴리오에 넣을 프로젝트를 선택하세요:

- ✅ 수업 프로젝트
- ✅ 개인 프로젝트
- ✅ 팀 프로젝트
- ✅ 해커톤 프로젝트
- ✅ 오픈소스 기여

**최소 2~3개** 프로젝트를 추천합니다.

### Step 3: 프로젝트 정보 정리

각 프로젝트마다 다음을 작성하세요:

#### 📋 작성 워크시트

**프로젝트 1**

```
□ ID: _______________
□ 제목: _______________
□ 설명 (2~3문장):
   ___________________________________
   ___________________________________
   ___________________________________

□ 주요 기술:
   - _______________
   - _______________
   - _______________

□ 링크: _______________
```

### Step 4: 프로젝트 폴더 생성 및 작성

#### 4-1. 새 프로젝트 폴더 생성

```bash
# 예: sentiment-analysis 프로젝트 추가
mkdir data/projects/sentiment-analysis
```

#### 4-2. project.json 작성

`data/projects/sentiment-analysis/project.json` 파일 생성:

```json
{
  "id": "sentiment-analysis",
  "title": "한국어 감정 분석 모델",
  "description": "BERT 기반 한국어 감정 분석 모델을 개발했습니다. 영화 리뷰 데이터셋을 활용하여 긍정/부정/중립을 분류하며, 정확도 89%를 달성했습니다. Hugging Face Transformers와 PyTorch를 사용하여 구현했습니다.",
  "tags": ["NLP", "BERT", "PyTorch", "Korean"],
  "link": "https://github.com/username/sentiment-analysis"
}
```

⚠️ **주의**: 배열 `[]`로 감싸지 않습니다! (단일 객체만)

#### 4-3. 빌드 실행

모든 프로젝트 폴더를 하나의 `projects.json`으로 통합:

```bash
python3 data/build.py
```

출력 예시:
```
📂 3개의 프로젝트 폴더를 발견했습니다.

✅ interlocutor-adaptation: Interlocutor Adaptation Dialogue System
✅ persona-scheduling: Dynamic Persona Scheduling Framework
✅ sentiment-analysis: 한국어 감정 분석 모델

🎉 성공! projects.json 파일이 생성되었습니다.
   총 3개의 프로젝트가 포함되었습니다.
```

생성된 `data/projects.json` 확인:

```bash
cat data/projects.json
```

---

## ✍️ 작성 가이드

### 1. ID 짓기

**좋은 예:**
- `rag-chatbot`
- `sentiment-analysis`
- `image-classifier`

**나쁜 예:**
- `프로젝트1` (한글 사용)
- `Project 1` (공백 사용)
- `my_super_awesome_project!!!` (특수문자 과다)

**규칙:**
- 영문 소문자
- 하이픈(-) 사용
- 간결하고 의미 있게

### 2. 제목 짓기

**좋은 예:**
- "RAG 기반 포트폴리오 챗봇"
- "실시간 객체 탐지 시스템"
- "대화형 AI 어시스턴트"

**팁:**
- 기술 키워드 포함
- 15자 이내 권장
- 명확하고 구체적으로

### 3. 설명 작성 (중요!)

**설명은 RAG 검색의 핵심 데이터입니다!**

#### 포함할 내용:
1. **무엇을** 만들었나?
2. **어떻게** 구현했나?
3. **결과**는 어땠나?

#### 예시:

**좋은 설명:**
```
ChromaDB와 Gemini를 활용한 RAG 기반 포트폴리오 챗봇을 개발했습니다.
프로젝트 문서를 벡터 임베딩하여 의미 기반 검색을 구현하고,
검색된 근거를 바탕으로 출처와 함께 답변을 생성합니다.
LangChain으로 파이프라인을 구축하고 FastAPI로 API 서버를 만들었습니다.
```

**나쁜 설명:**
```
챗봇을 만들었습니다.
```

#### 작성 팁:
- 2~4문장
- 구체적인 기술 이름 포함
- 성과/지표 포함 (가능하면)
- 검색 키워드 의식하며 작성

### 4. 태그 선정

**카테고리별 추천 태그:**

#### 기술 분야
- NLP, Computer Vision, Reinforcement Learning
- Machine Learning, Deep Learning, Data Analysis

#### 프레임워크/라이브러리
- PyTorch, TensorFlow, Scikit-learn
- LangChain, Hugging Face, OpenCV

#### 언어
- Python, JavaScript, SQL

#### 도메인
- Chatbot, Sentiment Analysis, Object Detection
- Recommendation System, Time Series

**팁:**
- 3~5개 권장
- 너무 일반적인 태그 지양 ("AI", "프로그래밍")
- 검색 가능한 구체적 키워드 사용

### 5. 링크 설정

**우선순위:**
1. GitHub 저장소
2. 배포된 데모 사이트
3. 프로젝트 문서/발표 자료
4. 없으면 `"#"` 또는 `""`

---

## 🧪 데이터 검증

### 빌드 스크립트 검증

`build.py`가 자동으로 검증합니다:

```bash
python3 data/build.py
```

**오류 예시:**

```
❌ Error: sentiment-analysis/project.json
   누락된 필드: description, tags
```

→ 해당 프로젝트의 `project.json`을 수정하세요.

**성공 예시:**

```
✅ sentiment-analysis: 한국어 감정 분석 모델
✅ image-classifier: 음식 이미지 분류 앱

🎉 성공! projects.json 파일이 생성되었습니다.
   총 2개의 프로젝트가 포함되었습니다.
```

### 수동 검증 (선택)

```bash
# 생성된 projects.json 검증
python3 -c "import json; print(json.load(open('data/projects.json')))"
```

정상이면 데이터가 출력됩니다.

### 온라인 도구 사용

개별 `project.json` 검증:

1. [JSONLint](https://jsonlint.com/) 접속
2. `data/projects/프로젝트명/project.json` 내용 복사
3. "Validate JSON" 클릭
4. 오류 있으면 수정 후 다시 빌드

---

## 📋 체크리스트

작성 완료 후 확인:

- [ ] 최소 2개 이상의 프로젝트 폴더 생성
- [ ] 각 폴더에 `project.json` 작성
- [ ] 모든 프로젝트에 `id`, `title`, `description`, `tags`, `link` 포함
- [ ] `id`는 영문 소문자 + 하이픈만 사용
- [ ] `description`은 2문장 이상, 구체적 기술 포함
- [ ] `tags`는 3~5개, 검색 가능한 키워드
- [ ] `python3 data/build.py` 실행 성공
- [ ] `data/projects.json` 파일 생성 확인

---

## 💡 FAQ

### Q1. 프로젝트가 없는데요?
A. 수업 과제, 스터디 프로젝트, 간단한 토이 프로젝트도 괜찮습니다. 중요한 것은 구조화된 데이터 작성 경험입니다.

### Q2. 설명을 얼마나 자세히 써야 하나요?
A. 2~4문장, 100~200자 정도가 적당합니다. 너무 짧으면 RAG 검색 성능이 떨어지고, 너무 길면 읽기 어렵습니다.

### Q3. 태그를 영어로 써야 하나요?
A. 영어 권장하지만 한글도 가능합니다. 단, 일관성 있게 사용하세요.

### Q4. description에 줄바꿈을 넣을 수 있나요?
A. JSON 문자열 안에서는 `\n`으로 줄바꿈 가능하지만, 검색 성능을 위해 하나의 문단으로 작성을 권장합니다.

### Q5. 나중에 수정할 수 있나요?
A. 언제든 가능합니다! 프로젝트 폴더의 `project.json`을 수정한 후 `python3 data/build.py`를 다시 실행하면 됩니다.

### Q6. 프로젝트를 추가하려면?
A.
```bash
# 1. 새 폴더 생성
mkdir data/projects/new-project

# 2. project.json 작성
# data/projects/new-project/project.json 파일 생성

# 3. 빌드
python3 data/build.py
```

### Q7. projects.json을 직접 수정하면 안 되나요?
A. 빌드 스크립트를 실행하면 덮어씌워지므로, 항상 `data/projects/` 폴더의 파일들을 수정하세요.

---

## 📖 예시 모음

### 예시 1: NLP 프로젝트

```json
{
  "id": "korean-qa-system",
  "title": "한국어 질의응답 시스템",
  "description": "KorQuAD 데이터셋을 활용하여 한국어 질의응답 모델을 개발했습니다. BERT 기반 모델을 파인튜닝하여 문맥에서 정답 범위를 추출하는 extractive QA를 구현했으며, F1 score 85%를 달성했습니다.",
  "tags": ["NLP", "Question Answering", "BERT", "Korean", "PyTorch"],
  "link": "https://github.com/username/korean-qa"
}
```

### 예시 2: Computer Vision 프로젝트

```json
{
  "id": "realtime-object-detection",
  "title": "실시간 객체 탐지 시스템",
  "description": "YOLOv8을 활용하여 웹캠 영상에서 실시간으로 객체를 탐지하는 시스템을 구축했습니다. OpenCV로 영상 스트리밍을 처리하고, 탐지된 객체 정보를 JSON으로 저장하는 기능을 추가했습니다. 초당 30프레임 처리 속도를 달성했습니다.",
  "tags": ["Computer Vision", "Object Detection", "YOLO", "OpenCV", "Real-time"],
  "link": "https://github.com/username/object-detection"
}
```

### 예시 3: 웹 개발 프로젝트

```json
{
  "id": "book-recommendation",
  "title": "독서 추천 웹 서비스",
  "description": "협업 필터링 알고리즘을 사용한 도서 추천 시스템입니다. Flask로 백엔드를 구현하고 React로 프론트엔드를 개발했습니다. 사용자의 독서 이력을 분석하여 유사한 취향의 사용자가 좋아한 책을 추천하며, PostgreSQL로 데이터를 관리합니다.",
  "tags": ["Recommendation System", "Flask", "React", "Collaborative Filtering"],
  "link": "https://book-rec.example.com"
}
```

---

## 🎉 다음 단계

`data/projects.json` 작성을 완료했나요?

✅ **완료했다면:**
👉 [02-WEBAPP.md](02-WEBAPP.md)로 이동하여 웹사이트를 만들어보세요!

❌ **막혔다면:**
- 예시를 참고하여 작성
- JSON 검증 도구로 형식 확인
- 일단 2개만 작성하고 진행 (나중에 추가 가능)
