// API 서버 주소 (학생들이 수정 가능)
const API_BASE_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    const widgetContainer = document.getElementById('chatbot-widget');

    // 챗봇 위젯 레이아웃 주입
    widgetContainer.innerHTML = `
        <div id="chatbot-header" class="chatbot-header">
            <span>💬 AI Research Assistant</span>
            <button id="chatbot-toggle-btn">-</button>
        </div>
        <div id="chatbot-body" class="chatbot-body">
            <div class="chatbot-messages" id="chatbot-messages">
                <div class="message system">
                    <strong>[안내]</strong> 프로젝트에 대해 무엇이든 물어보세요!
                </div>
            </div>
            <div class="chatbot-input-area">
                <input type="text" id="chatbot-input" placeholder="질문을 입력하세요...">
                <button id="chatbot-send-btn">전송</button>
            </div>
        </div>
    `;

    // DOM 요소 가져오기
    const toggleBtn = document.getElementById('chatbot-toggle-btn');
    const chatbotBody = document.getElementById('chatbot-body');
    const messagesDiv = document.getElementById('chatbot-messages');
    const inputField = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('chatbot-send-btn');

    // 토글 기능
    toggleBtn.addEventListener('click', () => {
        if (chatbotBody.style.display === 'none') {
            chatbotBody.style.display = 'flex';
            toggleBtn.textContent = '-';
        } else {
            chatbotBody.style.display = 'none';
            toggleBtn.textContent = '+';
        }
    });

    // 메시지 추가 함수
    function addMessage(content, type = 'user') {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);

        if (type === 'user') {
            messageDiv.innerHTML = `<strong>나:</strong> ${content}`;
        } else if (type === 'bot') {
            messageDiv.innerHTML = `<strong>AI:</strong> ${content}`;
        } else {
            messageDiv.innerHTML = content;
        }

        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    // 로딩 메시지 표시/제거
    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'system', 'loading');
        loadingDiv.id = 'loading-message';
        loadingDiv.innerHTML = '<strong>🔍 검색 중...</strong>';
        messagesDiv.appendChild(loadingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function removeLoading() {
        const loadingDiv = document.getElementById('loading-message');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }

    // 챗봇 API 호출
    async function sendQuestion(question) {
        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('API 호출 오류:', error);
            throw error;
        }
    }

    // 질문 전송 핸들러
    async function handleSendMessage() {
        const question = inputField.value.trim();

        if (!question) {
            return;
        }

        // 사용자 메시지 추가
        addMessage(question, 'user');
        inputField.value = '';

        // 로딩 표시
        showLoading();
        sendBtn.disabled = true;
        inputField.disabled = true;

        try {
            // API 호출
            const result = await sendQuestion(question);

            // 로딩 제거
            removeLoading();

            // AI 답변 추가
            addMessage(result.answer, 'bot');

            // 출처 표시 (있으면)
            if (result.sources && result.sources.length > 0) {
                const sourcesText = result.sources
                    .map((s, i) => `${i + 1}. ${s.title}`)
                    .join('<br>');
                addMessage(`<strong>📚 출처:</strong><br>${sourcesText}`, 'system');
            }

        } catch (error) {
            removeLoading();
            addMessage('❌ 오류가 발생했습니다. 서버가 실행 중인지 확인하세요.', 'system');
        } finally {
            sendBtn.disabled = false;
            inputField.disabled = false;
            inputField.focus();
        }
    }

    // 전송 버튼 클릭
    sendBtn.addEventListener('click', handleSendMessage);

    // Enter 키로 전송
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });
});
