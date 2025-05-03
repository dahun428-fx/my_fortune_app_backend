# app/llm/clova_llm.py
import logging
from app.llm.base import BaseLLM
from app.core.config import CLOVA_API_KEY, CLOVA_MODEL_NAME
from langchain_naver import ChatClovaX
from langchain.schema import HumanMessage

logger = logging.getLogger(__name__)


class ClovaLLM(BaseLLM):
    def __init__(self):
        self.llm = ChatClovaX(
            model=CLOVA_MODEL_NAME, api_key=CLOVA_API_KEY, temperature=0.7
        )

    def get_response(self, prompt: str) -> str:
        try:
            logger.debug("[DEBUG] Clova LLM 요청: %s", prompt)
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            logger.exception("[ERROR] Clova LLM 응답 실패")
            return f"[Clova Error] {str(e)}"
