# Step 2: 포트폴리오 웹앱 제작

`data/projects.json`을 읽어 동적으로 렌더링하는 포트폴리오 사이트 만들기

---

## 🎯 학습 목표

- Single Source of Truth 개념 이해
- Fetch API로 JSON 데이터 로드
- JavaScript로 동적 HTML 렌더링
- CSS로 개성 있는 디자인 커스터마이징
- 반응형 레이아웃 구현

---

## 📂 파일 구조

```
web/
├── index.html      # HTML 구조
├── app.js          # projects.json 로드 및 렌더링
├── style.css       # 스타일링
└── widget.js       # 챗봇 위젯 (3단계에서 활성화)

data/
└── projects.json   # 데이터 소스
```

---

## 🚀 빠른 시작

### Step 1: 예시 코드 실행

먼저 제공된 예시를 실행해보세요:

#### 예시 1: 심플 버전 (web1)

```bash
# examples/web1 폴더로 이동
cd web
# 간단한 HTTP 서버 실행
python3 -m http.server 8000
```

### Step 2: 본인 웹사이트 실행

```bash
# 프로젝트 루트로 이동
cd ../../

# web 폴더 실행
python3 -m http.server 8080
```

브라우저에서 http://localhost:8080/web/ 접속

---

## 📖 동작 원리 이해하기

### 1. HTML 구조 ([index.html](../web/index.html))

```html
<!DOCTYPE html>
<html>
<head>
    <title>My AI Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- 헤더 -->
    <header>
        <h1>내 이름</h1>
        <p>AI/ML 개발자</p>
    </header>

    <!-- 프로젝트 카드들이 렌더링될 공간 -->
    <main id="projects-container">
        <!-- JavaScript로 동적 생성됨 -->
    </main>

    <script src="app.js"></script>
</body>
</html>
```

### 2. JavaScript 로직 ([app.js](../web/app.js))

```javascript
// 1. projects.json 로드
fetch('../data/projects.json')
    .then(response => response.json())
    .then(projects => {
        // 2. 각 프로젝트를 카드로 렌더링
        projects.forEach(project => {
            const card = createProjectCard(project);
            container.appendChild(card);
        });
    });

// 3. 카드 HTML 생성
function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    card.innerHTML = `
        <h3>${project.title}</h3>
        <p>${project.description}</p>
        <div class="tags">
            ${project.tags.map(tag => `<span>${tag}</span>`).join('')}
        </div>
    `;
    return card;
}
```

### 3. 스타일링 ([style.css](../web/style.css))

```css
/* 프로젝트 카드 스타일 */
.project-card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.project-card h3 {
    color: #333;
    margin-bottom: 10px;
}

.tags span {
    background: #e3f2fd;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 0.9em;
}
```

---

## 🐛 문제 해결

### Q1. 프로젝트가 안 보여요!

**원인:** projects.json 경로 오류

**해결:**
```javascript
// app.js에서 경로 확인
fetch('../data/projects.json')  // 상대 경로 확인
```

브라우저 콘솔(F12)에서 네트워크 탭 확인

### Q2. 스타일이 안 먹혀요!

**원인:** CSS 파일 경로 오류 또는 선택자 오타

**해결:**
1. `<link href="style.css">`  경로 확인
2. 브라우저에서 F5로 강력 새로고침 (Ctrl+Shift+R)
3. 개발자 도구로 CSS 로드 확인

### Q3. localhost에서 CORS 에러가 나요!

**원인:** file:// 프로토콜로 열었을 때

**해결:**
```bash
# 반드시 HTTP 서버로 실행
python3 -m http.server 8080
```

-