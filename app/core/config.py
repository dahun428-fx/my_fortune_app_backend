import os
from dotenv import load_dotenv

# 기본은 .env 파일, 설정에 따라 .env.production 등
env_file = (
    ".env.development" if os.getenv("ENV") is None else f".env.{os.getenv('ENV')}"
)
load_dotenv(env_file)

# 환경변수 로드
load_dotenv(dotenv_path=env_file)

# 실제 설정값
DEBUG = os.getenv("DEBUG", "False") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # 기본값은 groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# app/core/config.py

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-pro")

CLOVA_API_KEY = os.getenv("CLOVA_API_KEY")
CLOVA_MODEL_NAME = os.getenv("CLOVA_MODEL_NAME")
