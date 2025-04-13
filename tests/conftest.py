# tests/conftest.py (파일이 없다면 새로 만드세요)
import os
from dotenv import load_dotenv

env_file = (
    ".env.development" if os.getenv("ENV") is None else f".env.{os.getenv('ENV')}"
)
load_dotenv(env_file)

ENV = os.getenv("ENV", "development")
DEBUG = os.getenv("DEBUG", "False") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # 기본값은 groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
