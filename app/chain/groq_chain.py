# app/chains/groq_chain.py
import logging
from app.llm.loader import load_llm

logger = logging.getLogger(__name__)


def get_fortune_llm_answer(prompt: str) -> str:
    llm = load_llm()
    result = llm.get_response(prompt)
    logger.debug("[DEBUG] LLM 응답: %s", result)
    return result
