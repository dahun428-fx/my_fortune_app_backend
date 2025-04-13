# app/chains/groq_chain.py
import logging
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from app.core.config import GROQ_API_KEY, GROQ_API_URL

logger = logging.getLogger(__name__)


def get_fortune_llm_answer(prompt: str) -> str:
    llm = ChatGroq(
        api_key=GROQ_API_KEY,  # 실제로는 settings.py에서 import
        model_name="llama-3.3-70b-versatile",
    )
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    logger.debug("[DEBUG] LLM 응답: %s", response.content)
    return response.content
