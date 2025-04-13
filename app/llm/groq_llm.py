# app/llm/groq_llm.py
import logging
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from app.llm.base import BaseLLM
from app.core.config import GROQ_API_KEY, GROQ_MODEL_NAME

logger = logging.getLogger(__name__)


class GroqLLM(BaseLLM):
    def __init__(self):
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=GROQ_MODEL_NAME,
            temperature=0.7,  # 필요 시 조절
        )

    def get_response(self, prompt: str) -> str:
        try:
            logger.debug("[DEBUG] Groq LLM 요청: %s", prompt)
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            logger.exception("[ERROR] Groq LLM 응답 실패")
            return f"[Groq Error] {str(e)}"
