# app/core/config.py
import os
from dotenv import load_dotenv

# 기본은 .env 파일, 설정에 따라 .env.production 등
env_file = ".env" if os.getenv("ENV") is None else f".env.{os.getenv('ENV')}"
load_dotenv(env_file)

ENV = os.getenv("ENV", "development")
DEBUG = os.getenv("DEBUG", "False") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
