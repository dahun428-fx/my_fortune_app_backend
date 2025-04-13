import os
from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")
env_file = f".env.{ENV}"

load_dotenv(dotenv_path=env_file, override=True)
