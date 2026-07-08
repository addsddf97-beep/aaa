# 배포 가이드

GitHub Actions + Render + GitHub Pages를 활용한 자동 배포

---

## 🏗️ 배포 아키텍처

```
┌─────────────────┐
│  GitHub (main)  │
└────────┬────────┘
         │ push
         ├──────────────────┬─────────────────┐
         ▼                  ▼                 ▼
  ┌─────────────┐   ┌──────────────┐  ┌─────────────┐
  │   GitHub    │   │    Render    │  │   GitHub    │
  │   Actions   │──▶│  (API 서버)   │  │    Pages    │
  └─────────────┘   └──────────────┘  └─────────────┘
                           │                  │
                           │                  │
                    FastAPI 백엔드        정적 프론트엔드
                    (챗봇 API)            (웹 페이지)
```

---

## 📋 배포 체크리스트

### 사전 준비
- [ ] GitHub 계정
- [ ] Render 계정 (무료)
- [ ] Gemini API 키

---

## 🚀 1단계: GitHub 저장소 생성

### 1. 로컬 Git 초기화

```bash
cd gbsw-ai-portfolio-template

# Git 초기화 (아직 안 했다면)
git init

# .gitignore 확인
cat .gitignore

# 파일 추가
git add .
git commit -m "Initial commit: RAG chatbot baseline"
```

### 2. GitHub에 Push

```bash
# GitHub에서 새 저장소 생성 후
git remote add origin https://github.com/YOUR_USERNAME/ai-portfolio.git
git branch -M main
git push -u origin main
```

---

## 🌐 2단계: Render 배포 (API 서버)

### 방법 1: render.yaml 사용 (추천)

1. **Render 대시보드 접속**
   - https://dashboard.render.com
   - "Sign up" 또는 "Log in with GitHub"

2. **New Blueprint Instance**
   - Dashboard → "New +" → "Blueprint"
   - Repository 연결
   - `render.yaml` 자동 감지됨

3. **환경 변수 설정**
   - Service 선택 → "Environment"
   - `GEMINI_API_KEY` 추가
   - Value: 발급받은 API 키 입력
   - "Save Changes"

4. **배포 확인**
   - "Deploy" 자동 시작
   - 로그에서 "✅ RAG 엔진 준비 완료!" 확인
   - URL: `https://ai-portfolio-api-xxxxx.onrender.com`

### 방법 2: 수동 설정

1. **New Web Service**
   - "New +" → "Web Service"
   - GitHub 저장소 선택

2. **설정 입력**
   ```
   Name: ai-portfolio-api
   Region: Oregon (US West)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn server.api:app --host 0.0.0.0 --port $PORT
   ```

3. **환경 변수 추가**
   - "Advanced" → "Add Environment Variable"
   - Key: `GEMINI_API_KEY`
   - Value: 발급받은 키

4. **Create Web Service**

### 배포 URL 확인

```bash
# 헬스체크
curl https://your-app.onrender.com/health

# 응답 예시
{"status": "healthy", "rag_engine": "ready"}
```

---

## 📄 3단계: GitHub Pages 배포 (프론트엔드)

### 1. GitHub Pages 활성화

1. **Repository Settings**
   - Settings → Pages
   - Source: "GitHub Actions" 선택
   - (기존 "Deploy from a branch" 대신)

2. **자동 배포**
   - `.github/workflows/deploy.yml` 파일로 자동 배포됨
   - main에 push하면 자동 실행

### 2. widget.js API URL 수정

배포 전 **반드시** API 주소를 Render URL로 변경:

```javascript
// web/widget.js 첫 줄
const API_BASE_URL = 'https://your-app.onrender.com';
```

### 3. 배포 확인

```bash
# 변경사항 커밋
git add web/widget.js
git commit -m "Update API URL for production"
git push origin main
```

**GitHub Actions 확인:**
- Repository → "Actions" 탭
- "Deploy to Render and GitHub Pages" 워크플로우 확인
- 녹색 체크 표시 → 성공!

**접속:**
- `https://YOUR_USERNAME.github.io/REPO_NAME`

---

## 🔄 4단계: 자동 배포 확인

### GitHub Actions 워크플로우

`.github/workflows/deploy.yml`이 다음을 자동 실행:

1. **main 브랜치 push 감지**
2. **백엔드**: Render가 자동 재배포
3. **프론트엔드**: GitHub Pages에 자동 배포

### 수동 배포 트리거

```bash
# GitHub Actions 탭에서
"Run workflow" → "Run workflow" 클릭
```

---

## 🧪 5단계: 배포 테스트

### 1. API 테스트

```bash
# 헬스체크
curl https://your-app.onrender.com/health

# 챗봇 API 테스트
curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "어떤 프로젝트를 했나요?"}'
```

### 2. 웹 페이지 테스트

1. GitHub Pages URL 접속
2. 우하단 챗봇 위젯 확인
3. 질문 입력 → 답변 수신 확인

---

## 🐛 문제 해결

### Render 배포 실패

**로그 확인:**
- Render Dashboard → Service → "Logs" 탭

**자주 발생하는 오류:**

1. **"GEMINI_API_KEY가 설정되지 않았습니다"**
   - Render → Environment → GEMINI_API_KEY 확인

2. **"requirements.txt not found"**
   - Build Command 확인: `pip install -r requirements.txt`

3. **"Module not found"**
   - Start Command 확인: `uvicorn server.api:app --host 0.0.0.0 --port $PORT`

### GitHub Pages 404 에러

**확인 사항:**
1. Repository → Settings → Pages → "GitHub Actions" 선택 확인
2. Actions 탭에서 배포 성공 여부 확인
3. `web/` 폴더에 `index.html` 존재 확인

### CORS 에러 (브라우저 콘솔)

**증상:**
```
Access to fetch at 'https://...' has been blocked by CORS policy
```

**해결:**
`server/api.py`에서 CORS 설정 확인:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 특정 도메인만
    ...
)
```

### 챗봇이 "서버가 실행 중인지 확인하세요"

**확인:**
1. `web/widget.js`의 `API_BASE_URL` 확인
2. Render 서버 상태 확인 (헬스체크)
3. 브라우저 콘솔에서 네트워크 오류 확인 (F12)

---

## 💰 비용 관리

### Render 무료 티어 제한

- **750시간/월** 실행 (하나의 서비스 기준 충분)
- **15분 비활성 시 슬립 모드** (첫 요청 시 재시작, 30초 소요)
- **월 100GB 대역폭**

### 슬립 모드 방지 (선택 사항)

무료로 깨우기:
```bash
# cron-job.org 또는 UptimeRobot 사용
# 5분마다 헬스체크 호출
curl https://your-app.onrender.com/health
```

---

## 🔐 보안 체크리스트

배포 전 반드시 확인:

- [ ] `.env` 파일이 `.gitignore`에 포함됨
- [ ] API 키가 코드에 하드코딩되지 않음
- [ ] `GEMINI_API_KEY`는 Render 환경변수로만 설정
- [ ] GitHub에 `.env` 파일이 올라가지 않았는지 확인

**만약 API 키가 GitHub에 노출되었다면:**
1. 즉시 키 재발급 (https://aistudio.google.com/apikey)
2. Render 환경변수 업데이트
3. 노출된 커밋 삭제 또는 저장소 Private 전환

---

## 📊 배포 모니터링

### Render 로그 확인

```bash
# 실시간 로그
Render Dashboard → Service → "Logs"

# 필터: "error", "failed" 등으로 검색
```

### GitHub Actions 로그

```bash
# Actions 탭 → 워크플로우 클릭 → Job 클릭
```

---

## 📚 참고 자료

- [Render 공식 문서](https://render.com/docs)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [GitHub Pages 가이드](https://docs.github.com/en/pages)
