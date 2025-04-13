import os
from dotenv import load_dotenv

# 명확한 기본값과 fallback 처리
ENV = os.getenv("ENV", "development")  # 기본값은 development
env_file = f".env.{ENV}"

# 환경변수 로드
load_dotenv(dotenv_path=env_file)

# 실제 설정값
DEBUG = os.getenv("DEBUG", "False") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
