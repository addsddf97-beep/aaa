# RAG 심화 선택 과제

이 문서는 `00_hello_llm.py`부터 `07_eval/`까지 공통 실습을 끝낸 뒤 진행하는 선택 과제 안내입니다.

목표는 단순히 기능을 많이 붙이는 것이 아니라, 자신의 포트폴리오 사이트를 **작동하는 작은 서비스**로 확장해 보는 것입니다.

## 📋 과제 개요

**전제 조건:**
- `00_hello_llm.py` ~ `07_eval` 실습 완료
- `/server`의 RAG 시스템을 자신의 포트폴리오에 맞게 수정
- 웹사이트에서 RAG 챗봇이 정상 작동하는 것 확인

**과제 요구사항:**
- 아래 9개 과제 중 **3개 이상 선택**하여 구현
- 각 과제는 독립적으로 구현 가능
- 자유롭게 변형 및 확장 가능

**제출할 때 꼭 보여줄 것:**
- 어떤 과제 3개를 선택했는지
- 어떤 파일을 수정했는지
- 실행 방법
- 실제 동작 화면 또는 짧은 영상
- 어려웠던 점과 해결 방법

---

## 빠른 선택 가이드

처음 서버 기능을 확장해보는 학생에게 추천:

```text
방명록 기록 + 프로젝트 좋아요/조회수
```

챗봇을 더 똑똑하게 만들고 싶은 학생에게 추천:

```text
질문 라우팅 시스템 + GitHub API 연동
```

포트폴리오를 관리 도구처럼 만들고 싶은 학생에게 추천:

```text
관리자 페이지 + 프로젝트 좋아요/조회수
```

구현 시간이 부족하면 먼저 **작게 동작하는 버전**을 완성한 뒤 확장하세요.

예:

```text
방명록: JSON 파일 저장 먼저 구현 → 나중에 SQLite로 확장
좋아요: 좋아요 증가만 먼저 구현 → 나중에 중복 방지 추가
라우팅: 키워드 기반 먼저 구현 → 나중에 LLM 분류로 확장
```

---

## 완료 기준

선택 과제 1개를 완료했다고 판단하려면 다음 4가지를 만족해야 합니다.

```text
1. 사용자가 웹 또는 API에서 기능을 직접 실행할 수 있다.
2. 기능 실행 결과가 화면이나 API 응답으로 확인된다.
3. 서버를 재시작해도 필요한 데이터가 유지된다. 단, 라우팅처럼 저장이 필요 없는 과제는 제외.
4. README 또는 제출 문서에 실행 방법과 수정 파일이 적혀 있다.
```

선택 과제 3개 이상이 위 기준을 만족하면 심화 과제 완료입니다.

---

## 📌 선택 과제 목록

### 1. 질문 라우팅 시스템 ⭐⭐⭐

질문 유형에 따라 RAG, 일반 LLM, 보류 응답으로 나누어 처리합니다.

### 2. 방명록 기록 ⭐⭐

방문자가 이름과 메시지를 남기고, 서버에 기록이 저장되게 합니다.

### 3. 프로젝트 좋아요/조회수 ⭐⭐

프로젝트별 조회수와 좋아요 수를 저장하고 웹 카드에 표시합니다.

### 4. GitHub API 연동 + Tool Use ⭐⭐⭐⭐

GitHub API로 스타 수, 최근 커밋, 언어 정보 등을 가져와 챗봇 답변에 활용합니다.

### 5. 관리자 페이지 (프로젝트 추가/삭제) ⭐⭐⭐⭐

포트폴리오 주인이 웹에서 프로젝트를 추가, 수정, 삭제할 수 있게 합니다.

### 6. 챗봇 답변 피드백 버튼 ⭐⭐

챗봇 답변 아래에 `도움됨 / 별로예요` 버튼을 추가합니다.

목표:
- 답변별 사용자 만족도 저장
- 어떤 질문에서 답변 품질이 낮은지 확인

예상 저장 데이터:

```json
{
  "question": "FastAPI 프로젝트 알려줘",
  "answer": "...",
  "feedback": "good",
  "created_at": "2026-07-08T10:00:00"
}
```

### 7. 챗봇 대화 기록 저장 ⭐⭐

사용자가 챗봇에 어떤 질문을 많이 하는지 저장합니다.

목표:
- 자주 묻는 질문 분석
- 포트폴리오에서 부족한 설명 찾기

확장:
- 관리자 페이지에서 최근 질문 목록 보기
- 많이 나온 질문 Top 5 표시

### 8. 프로젝트 추천 기능 ⭐⭐⭐

방문자가 관심사를 입력하면 관련 프로젝트를 추천합니다.

예시:

```text
사용자: 저는 백엔드와 API에 관심 있어요.
응답: 급식 만족도 분석 서비스와 AI 자기소개서 피드백 도구를 먼저 보면 좋습니다.
```

구현 힌트:
- 기존 RAG 검색 결과를 추천 목록처럼 보여주기
- 답변에 “추천 이유” 포함하기

### 9. RAG 평가 대시보드 + A/B 테스트 ⭐⭐⭐⭐⭐

07 평가셋을 활용해 프롬프트 A/B 테스트를 실행하고, 어떤 설정이 더 좋은지 대시보드로 비교합니다.

예시:
- 프롬프트 A: 짧고 간단한 답변
- 프롬프트 B: 프로젝트명과 근거를 반드시 포함하는 답변
- 평가 결과: `auto_pass`, `human_pass`, 평균 응답 길이, 실패 문항 비교

---

## 1️⃣ 질문 라우팅 시스템

### 🎯 목표
사용자의 질문 유형을 자동으로 분류하여 적절한 처리 방식을 선택하는 시스템을 만듭니다.

### 📖 배경
현재 RAG 시스템은 모든 질문에 대해 벡터 검색을 수행합니다. 하지만 "안녕하세요", "이름이 뭐예요?" 같은 질문은 프로젝트 문서를 검색할 필요가 없습니다. 질문을 분류하여 효율적으로 처리하면:
- 불필요한 검색 비용 절감
- 더 빠른 응답 속도
- 답변 품질 향상

### 💡 구현 시나리오

**질문 유형 3가지:**
1. **프로젝트 질문** → RAG 사용 (예: "NLP 프로젝트를 설명해줘")
2. **일반 대화** → 일반 LLM (예: "안녕", "날씨 어때?")
3. **답변 불가** → 정중하게 거절 (예: "희망 연봉은?")

### 📝 구현 예시

#### 1단계: 질문 분류기 만들기

`server/router.py` 파일 생성:

```python
"""
질문 라우팅 시스템
"""

from enum import Enum

class QuestionType(Enum):
    PROJECT = "project"      # RAG 사용
    GENERAL = "general"      # 일반 LLM
    UNKNOWN = "unknown"      # 답변 불가


class QuestionRouter:
    """질문 유형을 분류하는 라우터"""

    def __init__(self):
        # TODO: 프로젝트 관련 키워드 정의
        self.project_keywords = [
            "프로젝트", "project", "경험", "기술", "개발",
            "만든", "구현", "사용", "역할"
        ]

        # TODO: 일반 대화 패턴
        self.general_patterns = [
            "안녕", "hello", "hi", "감사", "thank"
        ]

        # TODO: 답변 불가 키워드
        self.unknown_keywords = [
            "연봉", "salary", "나이", "age", "전공", "대학"
        ]

    def classify(self, question: str) -> QuestionType:
        """
        질문을 분류합니다.

        TODO: 3가지 방법 중 선택하여 구현

        방법 1 (간단): 키워드 포함 여부로 분류
        방법 2 (중급): LLM에게 분류 요청 (Few-shot)
        방법 3 (고급): 분류 모델 학습 (sklearn)
        """
        question_lower = question.lower()

        # 방법 1 예시: 키워드 기반 분류
        # TODO: 학생이 구현

        # 힌트:
        # if any(keyword in question_lower for keyword in self.project_keywords):
        #     return QuestionType.PROJECT

        pass
```

#### 2단계: API에 라우터 적용

`server/api.py` 수정:

```python
from router import QuestionRouter, QuestionType

# 전역 변수에 라우터 추가
question_router = QuestionRouter()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    # TODO: 질문 분류
    question_type = question_router.classify(request.question)

    if question_type == QuestionType.PROJECT:
        # RAG 사용
        result = rag_engine.query(request.question)

    elif question_type == QuestionType.GENERAL:
        # TODO: 일반 LLM 응답 (RAG 없이)
        # 힌트: gemini API 직접 호출
        result = {
            "answer": "안녕하세요! 저는 포트폴리오 챗봇입니다. 프로젝트에 대해 궁금한 점을 물어보세요.",
            "sources": []
        }

    else:  # UNKNOWN
        # TODO: 정중한 거절 메시지
        result = {
            "answer": "죄송합니다. 프로젝트 관련 질문에만 답변할 수 있습니다.",
            "sources": []
        }

    return ChatResponse(
        answer=result['answer'],
        sources=result['sources']
    )
```

### ✅ 확인 방법

다음 질문들을 테스트하고 올바르게 분류되는지 확인:

```python
# 프로젝트 질문 (RAG 사용되어야 함)
"NLP 프로젝트를 설명해줘"
"FastAPI를 사용한 경험은?"
"팀 프로젝트에서 어떤 역할을 했나요?"

# 일반 대화 (간단한 응답)
"안녕하세요"
"고마워요"
"잘 부탁해"

# 답변 불가 (정중한 거절)
"희망 연봉은 얼마인가요?"
"대학교 전공이 뭐예요?"
"나이가 어떻게 되세요?"
```

### 🚀 확장 아이디어

1. **통계 대시보드**: 어떤 유형의 질문이 가장 많은지 분석
2. **학습 기반 분류**: 사용자 피드백으로 분류기 개선
3. **복합 질문 처리**: "안녕하세요, NLP 프로젝트를 설명해주세요" → 일반+프로젝트

### 💬 예상 결과

```
사용자: "안녕하세요"
챗봇: "안녕하세요! 저는 포트폴리오 챗봇입니다. 프로젝트에 대해 궁금한 점을 물어보세요."

사용자: "NLP 프로젝트를 설명해줘"
챗봇: "감정 분석 웹앱은 사용자가 입력한 텍스트의 감정을 분석하는 NLP 프로젝트입니다..."
      [출처: 감정 분석 웹앱]

사용자: "희망 연봉은 얼마인가요?"
챗봇: "죄송합니다. 프로젝트 관련 질문에만 답변할 수 있습니다."
```

---

## 2️⃣ 방명록 기록

### 🎯 목표
방문자가 포트폴리오에 메시지를 남길 수 있는 방명록 기능을 구현합니다.

### 📖 배경
포트폴리오를 본 사람들이 간단한 메시지를 남길 수 있으면:
- 사이트 활성화 느낌
- 방문자와의 소통
- 취업 시 네트워킹 기회

### 💡 구현 시나리오

**기능:**
1. 방문자가 이름과 메시지 입력
2. 서버에 저장
3. 메인 페이지에서 최근 방명록 조회
4. (선택) 욕설 필터링, 관리자 삭제 기능

**구현 방식 선택:**

수업 기본 추천은 JSON 파일 저장입니다. 현재 프로젝트 의존성만으로 바로 구현할 수 있습니다.

```text
data/guestbook.json
```

SQLite/SQLAlchemy를 사용하면 더 실제 서비스에 가깝지만, 추가 설치와 DB 개념이 필요합니다. 아래 예시는 DB 방식입니다. 어렵다면 JSON 파일 저장 방식으로 바꿔 구현해도 됩니다.

### 📝 구현 예시

#### 1단계: 데이터베이스 모델 정의

`server/database.py` 생성:

```python
"""
방명록 데이터베이스
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB 생성
DATABASE_URL = "sqlite:///./guestbook.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class GuestbookEntry(Base):
    """방명록 엔트리 모델"""
    __tablename__ = "guestbook"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    message = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "name": self.name,
            "message": self.message,
            "created_at": self.created_at.isoformat()
        }


# 테이블 생성
Base.metadata.create_all(bind=engine)


def get_db():
    """DB 세션 생성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 2단계: API 엔드포인트 추가

`server/api.py`에 추가:

```python
from database import GuestbookEntry, get_db
from sqlalchemy.orm import Session
from fastapi import Depends

# 요청 모델
class GuestbookRequest(BaseModel):
    name: str
    message: str


# 방명록 작성
@app.post("/guestbook")
async def create_guestbook(
    request: GuestbookRequest,
    db: Session = Depends(get_db)
):
    """
    방명록 작성

    TODO:
    1. 입력 검증 (이름 1-50자, 메시지 1-500자)
    2. 욕설 필터링 (선택)
    3. DB에 저장
    """

    # TODO: 입력 검증
    if not request.name or len(request.name) > 50:
        raise HTTPException(400, "이름은 1-50자여야 합니다.")

    if not request.message or len(request.message) > 500:
        raise HTTPException(400, "메시지는 1-500자여야 합니다.")

    # TODO: DB에 저장
    entry = GuestbookEntry(
        name=request.name,
        message=request.message
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {"success": True, "id": entry.id}


# 방명록 조회
@app.get("/guestbook")
async def get_guestbook(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    방명록 조회 (최신순)

    TODO: 최신순으로 limit개 조회
    """
    entries = db.query(GuestbookEntry)\
        .order_by(GuestbookEntry.created_at.desc())\
        .limit(limit)\
        .all()

    return {
        "entries": [entry.to_dict() for entry in entries],
        "total": db.query(GuestbookEntry).count()
    }
```

#### 3단계: 프론트엔드 UI

`index.html`에 방명록 섹션 추가:

```html
<!-- 방명록 섹션 -->
<section id="guestbook">
    <h2>방명록</h2>

    <!-- 방명록 작성 폼 -->
    <div class="guestbook-form">
        <input type="text" id="guest-name" placeholder="이름" maxlength="50">
        <textarea id="guest-message" placeholder="메시지를 남겨주세요" maxlength="500"></textarea>
        <button onclick="submitGuestbook()">작성</button>
    </div>

    <!-- 방명록 목록 -->
    <div id="guestbook-list"></div>
</section>
```

`app.js`에 함수 추가:

```javascript
// 방명록 작성
async function submitGuestbook() {
    const name = document.getElementById('guest-name').value.trim();
    const message = document.getElementById('guest-message').value.trim();

    // TODO: 입력 검증
    if (!name || !message) {
        alert('이름과 메시지를 입력해주세요.');
        return;
    }

    // TODO: API 호출
    try {
        const response = await fetch('http://localhost:8000/guestbook', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, message})
        });

        if (response.ok) {
            alert('방명록이 작성되었습니다!');
            // 폼 초기화 및 목록 새로고침
            document.getElementById('guest-name').value = '';
            document.getElementById('guest-message').value = '';
            loadGuestbook();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 방명록 조회
async function loadGuestbook() {
    // TODO: API 호출하여 방명록 목록 표시
    try {
        const response = await fetch('http://localhost:8000/guestbook?limit=10');
        const data = await response.json();

        const listDiv = document.getElementById('guestbook-list');
        listDiv.innerHTML = data.entries.map(entry => `
            <div class="guestbook-entry">
                <strong>${entry.name}</strong>
                <span class="date">${new Date(entry.created_at).toLocaleDateString()}</span>
                <p>${entry.message}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error:', error);
    }
}

// 페이지 로드 시 방명록 불러오기
document.addEventListener('DOMContentLoaded', loadGuestbook);
```

### ✅ 확인 방법

1. 서버 실행: `python server/api.py`
2. 웹페이지에서 방명록 작성
3. `guestbook.db` 파일 생성 확인
4. 작성한 방명록이 목록에 표시되는지 확인

### 🚀 확장 아이디어

1. **욕설 필터링**: 금지어 리스트로 필터링
2. **이모지 리액션**: 각 방명록에 좋아요 버튼
3. **관리자 삭제**: 관리자 비밀번호로 삭제 가능
4. **이미지 업로드**: 방명록에 이미지 첨부

### 💬 예상 결과

```
방명록 섹션:
┌────────────────────────────────┐
│ 방명록 작성                     │
│ 이름: [홍길동        ]          │
│ 메시지: [멋진 포트폴리오네요!]  │
│ [작성]                          │
└────────────────────────────────┘

최근 방명록:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
홍길동 | 2024-07-08
멋진 포트폴리오네요! 프로젝트들이 인상적입니다.

김철수 | 2024-07-07
NLP 프로젝트 대단하네요!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 3️⃣ 프로젝트 좋아요/조회수

### 🎯 목표
각 프로젝트별로 조회수와 좋아요 수를 추적하고 표시합니다.

### 📖 배경
프로젝트별 인기도를 파악하면:
- 어떤 프로젝트가 관심을 받는지 확인
- 방문자 참여 유도
- 포트폴리오 개선 방향 파악

### 💡 구현 시나리오

**기능:**
1. 프로젝트 카드 클릭 시 조회수 +1
2. 좋아요 버튼 클릭 시 좋아요 +1
3. 중복 방지 (쿠키 또는 localStorage)
4. 인기 프로젝트 순위 표시

### 📝 구현 예시

#### 1단계: 통계 관리 클래스

`server/stats.py` 생성:

```python
"""
프로젝트 통계 관리
"""

from collections import defaultdict
from typing import Dict, Set
import json
import os


class ProjectStats:
    """프로젝트별 조회수/좋아요 관리"""

    def __init__(self, persist_file: str = "project_stats.json"):
        self.persist_file = persist_file
        self.views: Dict[str, int] = defaultdict(int)
        self.likes: Dict[str, int] = defaultdict(int)
        self.liked_users: Dict[str, Set[str]] = defaultdict(set)

        # 기존 데이터 로드
        self.load()

    def increment_view(self, project_id: str):
        """조회수 증가"""
        self.views[project_id] += 1
        self.save()

    def toggle_like(self, project_id: str, user_id: str) -> bool:
        """
        좋아요 토글

        Returns:
            True: 좋아요 추가
            False: 좋아요 취소
        """
        # TODO: 사용자가 이미 좋아요 했는지 확인
        if user_id in self.liked_users[project_id]:
            # 좋아요 취소
            self.liked_users[project_id].remove(user_id)
            self.likes[project_id] -= 1
            self.save()
            return False
        else:
            # 좋아요 추가
            self.liked_users[project_id].add(user_id)
            self.likes[project_id] += 1
            self.save()
            return True

    def get_stats(self, project_id: str) -> Dict:
        """프로젝트 통계 조회"""
        return {
            "views": self.views[project_id],
            "likes": self.likes[project_id]
        }

    def get_all_stats(self) -> Dict:
        """모든 프로젝트 통계"""
        return {
            "views": dict(self.views),
            "likes": dict(self.likes)
        }

    def get_popular_projects(self, limit: int = 5) -> list:
        """인기 프로젝트 (좋아요순)"""
        sorted_projects = sorted(
            self.likes.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_projects[:limit]

    def save(self):
        """파일에 저장"""
        data = {
            "views": dict(self.views),
            "likes": dict(self.likes),
            "liked_users": {
                k: list(v) for k, v in self.liked_users.items()
            }
        }
        with open(self.persist_file, 'w') as f:
            json.dump(data, f)

    def load(self):
        """파일에서 로드"""
        if os.path.exists(self.persist_file):
            with open(self.persist_file, 'r') as f:
                data = json.load(f)
                self.views = defaultdict(int, data.get("views", {}))
                self.likes = defaultdict(int, data.get("likes", {}))
                self.liked_users = defaultdict(
                    set,
                    {k: set(v) for k, v in data.get("liked_users", {}).items()}
                )
```

#### 2단계: API 엔드포인트

`server/api.py`에 추가:

```python
from stats import ProjectStats

# 전역 변수
project_stats = ProjectStats()

@app.post("/projects/{project_id}/view")
async def view_project(project_id: str):
    """프로젝트 조회수 증가"""
    project_stats.increment_view(project_id)
    return project_stats.get_stats(project_id)


@app.post("/projects/{project_id}/like")
async def like_project(project_id: str, user_id: str):
    """
    프로젝트 좋아요 토글

    TODO: user_id는 프론트에서 생성하여 전달
    (쿠키 또는 localStorage에 저장된 UUID)
    """
    is_liked = project_stats.toggle_like(project_id, user_id)
    return {
        "liked": is_liked,
        **project_stats.get_stats(project_id)
    }


@app.get("/projects/stats")
async def get_all_stats():
    """모든 프로젝트 통계"""
    return project_stats.get_all_stats()


@app.get("/projects/popular")
async def get_popular_projects(limit: int = 5):
    """인기 프로젝트"""
    return {
        "popular": project_stats.get_popular_projects(limit)
    }
```

#### 3단계: 프론트엔드 연동

`app.js`에 추가:

```javascript
// 사용자 ID 생성 (localStorage에 저장)
function getUserId() {
    let userId = localStorage.getItem('userId');
    if (!userId) {
        userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('userId', userId);
    }
    return userId;
}

// 프로젝트 조회수 증가
async function incrementProjectView(projectId) {
    try {
        await fetch(`http://localhost:8000/projects/${projectId}/view`, {
            method: 'POST'
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// 좋아요 토글
async function toggleLike(projectId) {
    const userId = getUserId();

    try {
        const response = await fetch(
            `http://localhost:8000/projects/${projectId}/like?user_id=${userId}`,
            {method: 'POST'}
        );
        const data = await response.json();

        // UI 업데이트
        const likeBtn = document.querySelector(`[data-project-id="${projectId}"] .like-btn`);
        const likeCount = document.querySelector(`[data-project-id="${projectId}"] .like-count`);

        likeBtn.classList.toggle('liked', data.liked);
        likeCount.textContent = data.likes;

    } catch (error) {
        console.error('Error:', error);
    }
}

// 프로젝트 카드에 통계 표시
async function displayProjectStats() {
    try {
        const response = await fetch('http://localhost:8000/projects/stats');
        const stats = await response.json();

        // 각 프로젝트 카드에 통계 추가
        document.querySelectorAll('.project-card').forEach(card => {
            const projectId = card.dataset.projectId;
            const projectStats = {
                views: stats.views[projectId] || 0,
                likes: stats.likes[projectId] || 0
            };

            // TODO: 카드에 통계 표시
            const statsDiv = card.querySelector('.project-stats');
            if (statsDiv) {
                statsDiv.innerHTML = `
                    <span class="views">👁️ ${projectStats.views}</span>
                    <button class="like-btn" onclick="toggleLike('${projectId}')">
                        ❤️ <span class="like-count">${projectStats.likes}</span>
                    </button>
                `;
            }
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', displayProjectStats);
```

`index.html`의 프로젝트 카드에 추가:

```html
<div class="project-card" data-project-id="project-1" onclick="incrementProjectView('project-1')">
    <h3>프로젝트 제목</h3>
    <p>설명...</p>

    <!-- 통계 표시 영역 -->
    <div class="project-stats">
        <!-- JS로 동적 생성 -->
    </div>
</div>
```

### ✅ 확인 방법

1. 프로젝트 카드 클릭 → 조회수 증가 확인
2. 좋아요 버튼 클릭 → 좋아요 증가 확인
3. 다시 클릭 → 좋아요 감소 확인 (토글)
4. `project_stats.json` 파일에 데이터 저장 확인

### 🚀 확장 아이디어

1. **인기 순위**: 메인 페이지에 "인기 프로젝트 Top 5" 표시
2. **실시간 업데이트**: WebSocket으로 실시간 통계
3. **차트**: Chart.js로 통계 시각화
4. **기간별 통계**: 일간/주간/월간 조회수

### 💬 예상 결과

```
프로젝트 카드:
┌─────────────────────────────┐
│ NLP 감정 분석 웹앱           │
│ 사용자 텍스트 감정 분석...   │
│                              │
│ 👁️ 127  ❤️ 23              │
└─────────────────────────────┘

인기 프로젝트:
1. NLP 감정 분석 (❤️ 23)
2. 스마트 IoT 시스템 (❤️ 18)
3. 실시간 대시보드 (❤️ 15)
```

---

## 4️⃣ GitHub API 연동 + Tool Use

### 🎯 목표
Gemini의 Function Calling(Tool Use)을 활용하여 GitHub 정보를 실시간으로 가져와 답변합니다.

### 📖 배경
현재 RAG는 `projects.json`에 저장된 정적 데이터만 사용합니다. GitHub API를 연동하면:
- 실시간 스타 수, 이슈 수 등 최신 정보 제공
- 최근 커밋 내역 조회
- "가장 활발한 프로젝트는?" 같은 동적 질문 답변 가능

**Tool Use란?**
LLM이 필요할 때 외부 함수를 호출할 수 있게 하는 기능입니다. 예를 들어:
- 사용자: "GitHub 스타가 가장 많은 프로젝트는?"
- LLM: `get_github_stats()` 함수 호출 → API에서 데이터 받음 → 답변 생성

### 💡 구현 시나리오

**기능:**
1. GitHub API로 레포지토리 정보 가져오기
2. Gemini Function Calling으로 필요시 자동 호출
3. "최근 커밋은?", "스타 수는?" 같은 질문에 실시간 답변

### 📝 구현 예시

#### 1단계: GitHub API 클라이언트

`server/github_tools.py` 생성:

```python
"""
GitHub API 연동 도구
"""

import httpx
from typing import Dict


def get_github_stats(repo_url: str) -> Dict:
    """
    GitHub 레포지토리 통계 조회

    Args:
        repo_url: GitHub 레포지토리 URL (예: "https://github.com/user/repo")

    Returns:
        레포지토리 통계 (stars, forks, issues 등)
    """
    try:
        # URL에서 owner/repo 추출
        # "https://github.com/user/repo" → "user/repo"
        parts = repo_url.replace("https://github.com/", "").strip("/")

        # GitHub API 호출
        api_url = f"https://api.github.com/repos/{parts}"
        response = httpx.get(api_url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return {
                "name": data.get("name"),
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "language": data.get("language", "Unknown"),
                "description": data.get("description", ""),
                "last_updated": data.get("updated_at", "")
            }
        else:
            return {"error": f"API 호출 실패: {response.status_code}"}

    except Exception as e:
        return {"error": str(e)}


def get_recent_commits(repo_url: str, limit: int = 5) -> list:
    """
    최근 커밋 내역 조회

    Args:
        repo_url: GitHub 레포지토리 URL
        limit: 가져올 커밋 개수

    Returns:
        최근 커밋 목록
    """
    try:
        parts = repo_url.replace("https://github.com/", "").strip("/")
        api_url = f"https://api.github.com/repos/{parts}/commits"

        response = httpx.get(api_url, params={"per_page": limit}, timeout=5)

        if response.status_code == 200:
            commits = response.json()
            return [
                {
                    "message": commit["commit"]["message"],
                    "author": commit["commit"]["author"]["name"],
                    "date": commit["commit"]["author"]["date"]
                }
                for commit in commits
            ]
        else:
            return []

    except Exception as e:
        print(f"Error: {e}")
        return []


# Tool Use를 위한 함수 스키마 정의
GITHUB_TOOLS = [
    {
        "name": "get_github_stats",
        "description": "GitHub 레포지토리의 스타 수, 포크 수, 이슈 수 등 통계 정보를 가져옵니다. 사용자가 GitHub 관련 정보를 물어볼 때 사용하세요.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_url": {
                    "type": "string",
                    "description": "GitHub 레포지토리 URL (예: https://github.com/user/repo)"
                }
            },
            "required": ["repo_url"]
        }
    },
    {
        "name": "get_recent_commits",
        "description": "GitHub 레포지토리의 최근 커밋 내역을 가져옵니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_url": {
                    "type": "string",
                    "description": "GitHub 레포지토리 URL"
                },
                "limit": {
                    "type": "integer",
                    "description": "가져올 커밋 개수 (기본값: 5)"
                }
            },
            "required": ["repo_url"]
        }
    }
]
```

#### 2단계: RAG에 Tool Use 통합

`server/rag_core.py` 수정:

```python
from github_tools import get_github_stats, get_recent_commits, GITHUB_TOOLS
import google.generativeai as genai

class RAGEngine:
    def query_with_tools(self, question: str) -> dict:
        """
        Tool Use 지원 RAG 쿼리

        TODO: Gemini Function Calling 구현
        """
        # 1. 문서 검색 (기존 RAG)
        docs = self.retriever.get_relevant_documents(question)
        context = "\n\n".join([doc.page_content for doc in docs])

        # 2. 프롬프트 생성
        prompt = f"""
당신은 포트폴리오 AI 어시스턴트입니다.

사용 가능한 도구:
- get_github_stats: GitHub 레포지토리 통계 조회
- get_recent_commits: 최근 커밋 내역 조회

프로젝트 문서:
{context}

질문: {question}

답변:
"""

        # 3. Gemini에 도구 등록하여 호출
        # TODO: 학생이 Gemini Function Calling 문서 참고하여 구현
        # 힌트: model.generate_content(prompt, tools=GITHUB_TOOLS)

        # 4. 도구 호출 결과 처리
        # LLM이 도구를 호출하면 실제 함수 실행 → 결과 반환

        pass
```

#### 3단계: API 엔드포인트 추가

`server/api.py`에 추가:

```python
@app.get("/github/stats")
async def github_stats(repo_url: str):
    """GitHub 레포지토리 통계 조회"""
    from github_tools import get_github_stats
    return get_github_stats(repo_url)


@app.post("/chat/tools")
async def chat_with_tools(request: ChatRequest):
    """
    Tool Use 지원 챗봇

    TODO: RAG + GitHub Tool 통합
    """
    result = rag_engine.query_with_tools(request.question)
    return result
```

### ✅ 확인 방법

다음 질문들로 테스트:

```python
# GitHub 정보 질문
"NLP 프로젝트의 GitHub 스타는 몇 개야?"
"가장 최근 커밋은 언제 했어?"
"어떤 프로젝트가 가장 활발하게 관리되고 있어?"

# 일반 + GitHub 혼합
"FastAPI를 사용한 프로젝트의 GitHub 통계를 알려줘"
```

### 🚀 확장 아이디어

1. **자동 배지 생성**: README에 스타 수 배지 자동 추가
2. **기여자 정보**: 프로젝트 기여자 목록 표시
3. **언어 비율**: GitHub에서 언어 비율 가져와 차트로 표시
4. **이슈 트래커**: 열린 이슈 목록 표시

### 💬 예상 결과

```
사용자: "NLP 프로젝트의 GitHub 스타는 몇 개야?"

챗봇: "NLP 감정 분석 프로젝트는 현재 GitHub에서 ⭐ 23개의 스타를 받았습니다.
       또한 🍴 5개의 포크와 📝 2개의 열린 이슈가 있습니다.
       마지막 업데이트는 2024-07-05입니다."

       [출처: GitHub API 실시간 조회]
```

### 📚 참고 자료

- Gemini Function Calling: https://ai.google.dev/docs/function_calling
- GitHub REST API: https://docs.github.com/en/rest

---

## 5️⃣ 관리자 페이지 (프로젝트 추가/삭제)

### 🎯 목표
관리자(포트폴리오 주인)가 웹 UI에서 프로젝트를 추가/수정/삭제할 수 있는 관리자 페이지를 만듭니다.

### 📖 배경
현재는 `projects.json` 파일을 직접 수정해야 프로젝트를 관리할 수 있습니다. 관리자 페이지가 있으면:
- JSON 파일 수정 없이 웹에서 프로젝트 관리
- 실시간 RAG 업데이트 (벡터 DB 재구축)
- 비개발자도 쉽게 관리 가능

### 💡 구현 시나리오

**기능:**
1. 관리자 로그인 (간단한 비밀번호 인증)
2. 프로젝트 목록 조회 (CRUD)
3. 프로젝트 추가/수정/삭제
4. 변경 시 자동으로 RAG 재구축

### 📝 구현 예시

#### 1단계: 관리자 인증

`server/auth.py` 생성:

```python
"""
간단한 관리자 인증
"""

import os
from fastapi import HTTPException, Header
from dotenv import load_dotenv

load_dotenv()

# 환경변수에서 관리자 비밀번호 로드
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin1234")


def verify_admin(authorization: str = Header(None)):
    """
    관리자 권한 확인

    Header: Authorization: Bearer {password}
    """
    if not authorization:
        raise HTTPException(401, "인증이 필요합니다.")

    # "Bearer {password}" 형식에서 비밀번호 추출
    try:
        scheme, password = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(401, "잘못된 인증 형식입니다.")

        if password != ADMIN_PASSWORD:
            raise HTTPException(401, "비밀번호가 틀렸습니다.")

    except ValueError:
        raise HTTPException(401, "잘못된 인증 형식입니다.")
```

#### 2단계: 프로젝트 관리 API

`server/api.py`에 추가:

```python
from auth import verify_admin
import json
from pathlib import Path

# 프로젝트 모델
class ProjectModel(BaseModel):
    id: str
    title: str
    description: str
    role: str
    period: str
    skills: list
    achievements: list
    link: Optional[str] = None


@app.get("/admin/projects", dependencies=[Depends(verify_admin)])
async def get_all_projects():
    """
    모든 프로젝트 조회 (관리자용)
    """
    projects_path = Path("../data/projects.json")
    with open(projects_path, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    return {"projects": projects}


@app.post("/admin/projects", dependencies=[Depends(verify_admin)])
async def create_project(project: ProjectModel):
    """
    프로젝트 추가

    TODO:
    1. projects.json 읽기
    2. 새 프로젝트 추가
    3. projects.json 저장
    4. RAG 재구축
    """
    projects_path = Path("../data/projects.json")

    # 1. 기존 프로젝트 로드
    with open(projects_path, 'r', encoding='utf-8') as f:
        projects = json.load(f)

    # 2. 새 프로젝트 추가
    projects.append(project.dict())

    # 3. 저장
    with open(projects_path, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)

    # 4. RAG 재구축
    global rag_engine
    rag_engine = build_rag_engine(
        projects_json_path=str(projects_path),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        rebuild=True  # 강제 재구축
    )

    return {"success": True, "message": "프로젝트가 추가되었습니다."}


@app.put("/admin/projects/{project_id}", dependencies=[Depends(verify_admin)])
async def update_project(project_id: str, project: ProjectModel):
    """
    프로젝트 수정

    TODO: 프로젝트 ID로 찾아서 수정
    """
    # TODO: 학생이 구현
    pass


@app.delete("/admin/projects/{project_id}", dependencies=[Depends(verify_admin)])
async def delete_project(project_id: str):
    """
    프로젝트 삭제

    TODO: 프로젝트 ID로 찾아서 삭제
    """
    projects_path = Path("../data/projects.json")

    # 1. 기존 프로젝트 로드
    with open(projects_path, 'r', encoding='utf-8') as f:
        projects = json.load(f)

    # 2. 해당 프로젝트 삭제
    projects = [p for p in projects if p.get("id") != project_id]

    # 3. 저장
    with open(projects_path, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)

    # 4. RAG 재구축
    global rag_engine
    rag_engine = build_rag_engine(
        projects_json_path=str(projects_path),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        rebuild=True
    )

    return {"success": True, "message": "프로젝트가 삭제되었습니다."}
```

#### 3단계: 관리자 페이지 UI

`admin.html` 생성:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>관리자 페이지</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .login-form {
            max-width: 300px;
            margin: 100px auto;
        }

        .project-list {
            display: grid;
            gap: 20px;
        }

        .project-item {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 8px;
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }

        .btn-primary { background: #007bff; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-success { background: #28a745; color: white; }
    </style>
</head>
<body>
    <!-- 로그인 폼 -->
    <div id="login-section" class="login-form">
        <h2>관리자 로그인</h2>
        <input type="password" id="password" placeholder="비밀번호">
        <button class="btn btn-primary" onclick="login()">로그인</button>
    </div>

    <!-- 관리자 페이지 (로그인 후 표시) -->
    <div id="admin-section" style="display: none;">
        <h1>프로젝트 관리</h1>

        <button class="btn btn-success" onclick="showAddForm()">➕ 새 프로젝트</button>

        <!-- 프로젝트 추가 폼 (토글) -->
        <div id="add-form" style="display: none; margin: 20px 0; padding: 20px; border: 1px solid #ddd;">
            <h3>프로젝트 추가</h3>
            <input type="text" id="project-id" placeholder="ID (예: project-4)"><br>
            <input type="text" id="project-title" placeholder="제목"><br>
            <textarea id="project-description" placeholder="설명" rows="3"></textarea><br>
            <input type="text" id="project-role" placeholder="역할"><br>
            <input type="text" id="project-period" placeholder="기간"><br>
            <input type="text" id="project-skills" placeholder="기술 (쉼표로 구분)"><br>
            <textarea id="project-achievements" placeholder="성과 (한 줄씩)" rows="3"></textarea><br>
            <input type="text" id="project-link" placeholder="GitHub 링크 (선택)"><br>

            <button class="btn btn-success" onclick="createProject()">추가</button>
            <button class="btn" onclick="hideAddForm()">취소</button>
        </div>

        <!-- 프로젝트 목록 -->
        <div id="project-list" class="project-list"></div>
    </div>

    <script>
        let authToken = '';

        // 로그인
        async function login() {
            const password = document.getElementById('password').value;

            // 비밀번호를 Bearer 토큰으로 사용
            authToken = password;

            // 프로젝트 목록 조회로 인증 확인
            try {
                const response = await fetch('http://localhost:8000/admin/projects', {
                    headers: {
                        'Authorization': `Bearer ${authToken}`
                    }
                });

                if (response.ok) {
                    document.getElementById('login-section').style.display = 'none';
                    document.getElementById('admin-section').style.display = 'block';
                    loadProjects();
                } else {
                    alert('비밀번호가 틀렸습니다.');
                }
            } catch (error) {
                alert('서버 연결 실패');
            }
        }

        // 프로젝트 목록 로드
        async function loadProjects() {
            const response = await fetch('http://localhost:8000/admin/projects', {
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });

            const data = await response.json();
            const listDiv = document.getElementById('project-list');

            listDiv.innerHTML = data.projects.map(project => `
                <div class="project-item">
                    <h3>${project.title}</h3>
                    <p><strong>ID:</strong> ${project.id}</p>
                    <p><strong>설명:</strong> ${project.description}</p>
                    <p><strong>역할:</strong> ${project.role}</p>
                    <p><strong>기간:</strong> ${project.period}</p>
                    <p><strong>기술:</strong> ${project.skills.join(', ')}</p>

                    <button class="btn btn-primary" onclick="editProject('${project.id}')">수정</button>
                    <button class="btn btn-danger" onclick="deleteProject('${project.id}')">삭제</button>
                </div>
            `).join('');
        }

        // 추가 폼 표시
        function showAddForm() {
            document.getElementById('add-form').style.display = 'block';
        }

        function hideAddForm() {
            document.getElementById('add-form').style.display = 'none';
        }

        // 프로젝트 추가
        async function createProject() {
            const project = {
                id: document.getElementById('project-id').value,
                title: document.getElementById('project-title').value,
                description: document.getElementById('project-description').value,
                role: document.getElementById('project-role').value,
                period: document.getElementById('project-period').value,
                skills: document.getElementById('project-skills').value.split(',').map(s => s.trim()),
                achievements: document.getElementById('project-achievements').value.split('\n').filter(s => s.trim()),
                link: document.getElementById('project-link').value
            };

            // TODO: 입력 검증

            const response = await fetch('http://localhost:8000/admin/projects', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify(project)
            });

            if (response.ok) {
                alert('프로젝트가 추가되었습니다!');
                hideAddForm();
                loadProjects();
            } else {
                alert('추가 실패');
            }
        }

        // 프로젝트 삭제
        async function deleteProject(projectId) {
            if (!confirm('정말 삭제하시겠습니까?')) return;

            const response = await fetch(`http://localhost:8000/admin/projects/${projectId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });

            if (response.ok) {
                alert('프로젝트가 삭제되었습니다!');
                loadProjects();
            } else {
                alert('삭제 실패');
            }
        }

        // 프로젝트 수정 (TODO)
        function editProject(projectId) {
            alert('수정 기능은 TODO로 남겨둡니다. 학생이 구현해보세요!');
        }
    </script>
</body>
</html>
```

### ✅ 확인 방법

1. `.env`에 관리자 비밀번호 설정:
   ```
   ADMIN_PASSWORD=mysecret123
   ```

2. 서버 실행 후 `admin.html` 열기

3. 비밀번호 입력하여 로그인

4. 프로젝트 추가/삭제 테스트

5. 챗봇에서 새로 추가한 프로젝트 질문하여 RAG 업데이트 확인

### 🚀 확장 아이디어

1. **이미지 업로드**: 프로젝트 썸네일 이미지 업로드
2. **일괄 수정**: 여러 프로젝트 한 번에 수정
3. **백업/복원**: projects.json 백업 다운로드
4. **통계 대시보드**: 프로젝트별 조회수, 좋아요 차트

### 💬 예상 결과

```
관리자 페이지:

┌────────────────────────────────┐
│ 관리자 로그인                   │
│ 비밀번호: [**********]          │
│ [로그인]                        │
└────────────────────────────────┘

로그인 후:

프로젝트 관리                [➕ 새 프로젝트]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NLP 감정 분석 웹앱
ID: project-1
설명: 사용자 입력 텍스트의 감정을 분석...
역할: 백엔드 개발, NLP 모델 튜닝
기간: 2024.01 ~ 2024.03
기술: Python, FastAPI, Transformers

[수정] [삭제]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 9️⃣ RAG 평가 대시보드 + A/B 테스트

### 🎯 목표
07 평가 파이프라인을 확장하여, 서로 다른 RAG 설정을 비교하는 실험 시스템을 만듭니다.

### 📖 배경
RAG는 프롬프트, `k`, `chunk_size`, 멀티쿼리 방식에 따라 결과가 달라집니다. 감으로 “좋아진 것 같다”고 판단하지 않고, 같은 평가셋으로 여러 설정을 비교하면 더 설득력 있게 튜닝할 수 있습니다.

### 💡 구현 시나리오

**기능:**
1. 프롬프트 A/B 두 가지 준비
2. 같은 `eval_dataset.json`으로 두 설정 실행
3. 각 설정의 자동 평가 점수 저장
4. 실패 문항 비교
5. 간단한 HTML 또는 터미널 표로 결과 표시

### 📝 구현 예시

#### 1단계: 실험 설정 파일 만들기

`lessons/rag-handout/07_eval/experiment_config.json` 생성:

```json
[
  {
    "name": "A_basic",
    "k": 3,
    "prompt_style": "basic"
  },
  {
    "name": "B_source_required",
    "k": 4,
    "prompt_style": "source_required"
  }
]
```

#### 2단계: 평가 실행 결과 저장

`evaluate.py`를 확장하거나 새 파일 `run_experiments.py`를 만듭니다.

```python
def run_experiment(config):
    """
    TODO:
    1. config의 k와 prompt_style 적용
    2. eval_dataset.json 전체 실행
    3. pass 개수와 실패 문항 저장
    """
    return {
        "name": config["name"],
        "auto_pass": 5,
        "total": 7,
        "failed_ids": ["hard_04_school_services_rank"]
    }
```

#### 3단계: 결과 비교 출력

터미널 출력 예시:

```text
실험 결과

A_basic            PASS 5/7   실패: hard_02, hard_04
B_source_required  PASS 6/7   실패: hard_04

추천 설정: B_source_required
이유: 출처와 핵심 키워드 포함률이 더 높음
```

웹 대시보드로 확장할 수도 있습니다.

```text
GET /eval/results
```

### ✅ 확인 방법

1. `experiment_config.json`에 실험 설정 2개 이상 작성
2. `run_experiments.py` 실행
3. 각 설정의 PASS 개수와 실패 문항이 출력되는지 확인
4. 어떤 설정이 더 좋은지 설명

### 🚀 확장 아이디어

1. **프롬프트 비교**: 친절한 답변 vs 짧은 답변
2. **검색 개수 비교**: `k=2`, `k=3`, `k=5`
3. **멀티쿼리 비교**: 원 질문만 사용 vs query_variants 사용
4. **시각화**: Chart.js로 설정별 PASS 비율 그래프 표시
5. **사람 평가 반영**: `human_pass`까지 포함해 최종 점수 계산

### 💬 예상 결과

```
최종 보고서:

실험한 설정:
- A_basic: k=3, 기본 프롬프트
- B_source_required: k=4, 출처 필수 프롬프트

결과:
- A_basic: 5/7 통과
- B_source_required: 6/7 통과

분석:
B 설정은 답변에 프로젝트명을 더 자주 포함했지만, 응답이 길어지는 단점이 있었다.
```

---

## 📤 제출 가이드

### 제출물 체크리스트

- [ ] GitHub 레포지토리 링크
- [ ] README.md에 다음 내용 포함:
  - [ ] 선택한 과제 3개 이상 명시
  - [ ] 각 과제별 구현 내용 설명
  - [ ] 동작 화면 캡처 또는 GIF
  - [ ] 어려웠던 점 및 해결 방법
- [ ] 코드가 정상 실행되는지 확인
- [ ] `.env` 파일은 제외 (`.env.example`로 샘플 제공)

### README.md 예시

```markdown
# RAG 포트폴리오 - 심화 과제

## 선택 과제
1. 질문 라우팅 시스템
2. 프로젝트 좋아요/조회수

## 1. 질문 라우팅 시스템

### 구현 내용
- 질문을 3가지 유형으로 분류 (프로젝트/일반/답변불가)
- 키워드 기반 분류 알고리즘 구현
- 분류에 따라 다른 응답 방식 적용

### 실행 방법
\`\`\`bash
python server/api.py
\`\`\`

### 동작 화면
![질문 라우팅](screenshots/routing.png)

### 어려웠던 점
- 애매한 질문 분류 (예: "FastAPI 좋아해?")
- 해결: 키워드 우선순위 부여 및 기본값을 일반 대화로 설정

## 2. 프로젝트 좋아요/조회수

### 구현 내용
...
```

---

## 🙋 FAQ

**Q1: 3개 이상 선택해야 하나요?**
A: 네, 최소 3개 선택이 필수입니다. 더 많이 해도 좋습니다!

**Q2: 코드를 완전히 다르게 구현해도 되나요?**
A: 네! 제공된 코드는 예시일 뿐이며, 자유롭게 변형 가능합니다.

**Q3: 과제를 합쳐도 되나요?**
A: 가능합니다. 예: "관리자 페이지 + 프로젝트 통계" 통합

**Q4: 평가 기준은?**
A:
- 기능 구현 완성도 (50%)
- 코드 품질 및 주석 (20%)
- README 문서화 (20%)
- 창의성 및 확장 (10%)

**Q5: 막히면 어떻게 하나요?**
A:
1. 에러 메시지를 Google에 검색
2. 공식 문서 확인 (FastAPI, Gemini API 등)
3. 동료와 토론 (코드 복사는 X, 아이디어 공유는 O)
4. 강사에게 질문

---

## 📚 참고 자료

### API 문서
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Gemini API 문서](https://ai.google.dev/docs)
- [GitHub REST API](https://docs.github.com/en/rest)

### 튜토리얼
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

### 도구
- [Postman](https://www.postman.com/) - API 테스트
- [DB Browser for SQLite](https://sqlitebrowser.org/) - DB 확인

---

**행운을 빕니다! 🚀**

궁금한 점이 있으면 언제든지 질문하세요.
