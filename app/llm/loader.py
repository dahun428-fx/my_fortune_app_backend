from app.llm.base import BaseLLM
from app.llm.groq_llm import GroqLLM
from app.llm.gemini_llm import GeminiLLM  # ✅ 추가

from app.core.config import LLM_PROVIDER


def load_llm() -> BaseLLM:
    if LLM_PROVIDER == "groq":
        return GroqLLM()
    elif LLM_PROVIDER == "gemini":  # ✅ 추가
        return GeminiLLM()
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
