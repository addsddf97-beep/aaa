"""
실습 0: 환경 설정과 첫 LLM 호출

목표:
- .env에서 GEMINI_API_KEY를 읽습니다.
- Gemini 모델에 짧은 질문을 보내고 답변을 출력합니다.
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# TODO 1: ChatGoogleGenerativeAI로 LLM 객체를 만드세요.
# 힌트: model="gemini-2.5-flash"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# TODO 2: llm.invoke(...)로 짧은 인사 요청을 보내세요.
answer = llm.invoke("안녕하세요! 간단한 인사 한마디 부탁드려요.")

# TODO 3: 응답의 텍스트만 출력하세요.
# 힌트: answer.content
print(answer.content)
