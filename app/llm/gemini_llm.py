# app/llm/gemini_llm.py
import logging
from app.llm.base import BaseLLM
from app.core.config import GEMINI_API_KEY, GEMINI_MODEL_NAME
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

logger = logging.getLogger(__name__)


class GeminiLLM(BaseLLM):
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL_NAME, google_api_key=GEMINI_API_KEY, temperature=0.7
        )

    def get_response(self, prompt: str) -> str:
        try:
            logger.debug("[DEBUG] GEMINI LLM 요청: %s", prompt)
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            logger.exception("[ERROR] GEMINI LLM 응답 실패")
            return f"[Gemini Error] {str(e)}"
