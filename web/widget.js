// API 서버 주소
const API_BASE_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    const widgetContainer = document.getElementById('chatbot-widget');
    if (!widgetContainer) return;

    // 챗봇 위젯 레이아웃 주입
    widgetContainer.innerHTML = `
        <div id="chatbot-header" class="chatbot-header">
            <span>AI Assistant</span>
        </div>
        <div id="chatbot-body" class="chatbot-body">
            <div class="chatbot-messages" id="chatbot-messages">
                <div class="chat-row system">
                    <div class="message system">
                        <strong>[안내]</strong> 이력 및 프로젝트에 대해 무엇이든 물어보세요!
                    </div>
                </div>
            </div>
            <div class="chatbot-input-area">
                <input type="text" id="chatbot-input" placeholder="질문을 입력하세요...">
                <button id="chatbot-send-btn">전송</button>
            </div>
        </div>
    `;

    const messagesDiv = document.getElementById('chatbot-messages');
    const inputField = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('chatbot-send-btn');

    // 메시지 추가 함수 (정렬 처리를 위해 chat-row 래퍼 추가)
    function addMessage(content, type = 'user') {
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('chat-row', type); // user 또는 bot 클래스 부여

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);

        if (type === 'user') {
            messageDiv.innerHTML = `${content}`;
        } else if (type === 'bot') {
            messageDiv.innerHTML = `<strong>AI:</strong> ${content}`;
        } else {
            messageDiv.innerHTML = content;
        }

        rowDiv.appendChild(messageDiv);
        messagesDiv.appendChild(rowDiv);
        
        // 스크롤을 항상 최하단으로 이동
        setTimeout(() => {
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }, 10);
    }

    // 로딩 표시
    function showLoading() {
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('chat-row', 'system');
        rowDiv.id = 'loading-message';

        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'system');
        loadingDiv.innerHTML = '<strong>🔍 답변을 생성하는 중...</strong>';
        
        rowDiv.appendChild(loadingDiv);
        messagesDiv.appendChild(rowDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function removeLoading() {
        const loadingMessage = document.getElementById('loading-message');
        if (loadingMessage) loadingMessage.remove();
    }

    // 챗봇 API 호출
    async function sendQuestion(question) {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        if (!response.ok) throw new Error();
        return await response.json();
    }

    // 질문 전송 핸들러
    async function handleSendMessage() {
        const question = inputField.value.trim();
        if (!question) return;

        addMessage(question, 'user');
        inputField.value = '';
        

        showLoading();
        sendBtn.disabled = true;
        inputField.disabled = true;

        try {
            const result = await sendQuestion(question);
            removeLoading();
            addMessage(result.answer, 'bot');

            if (result.sources && result.sources.length > 0) {
                const sourcesText = result.sources.map((s, i) => `${i + 1}. ${s.title}`).join('<br>');
                addMessage(`<strong>📚 출처:</strong><br>${sourcesText}`, 'system');
            }
        } catch (error) {
            removeLoading();
            addMessage('❌ 오류가 발생했습니다. 서버 상태를 확인하세요.', 'system');
        } finally {
            sendBtn.disabled = false;
            inputField.disabled = false;
            inputField.focus();
        }
    }

    sendBtn.addEventListener('click', handleSendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSendMessage();
    });
});


