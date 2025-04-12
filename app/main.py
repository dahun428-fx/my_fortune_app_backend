from fastapi import FastAPI
from app.api.v1 import fortune

app = FastAPI()

app.include_router(fortune.router, prefix="/api/v1")
