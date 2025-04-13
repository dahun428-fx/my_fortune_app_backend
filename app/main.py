# app/main.py

import os
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1 import fortune
from app.logging_config import setup_logging

# 환경 감지 (default: development)
ENV_MODE = os.getenv("ENV", "development")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

# 로깅 설정
setup_logging()

app = FastAPI()

# 🌐 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(fortune.router, prefix="/api/v1")


# 🧩 유효성 검사 오류 응답
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    def clean_errors(errors):
        for err in errors:
            if "ctx" in err and isinstance(err["ctx"].get("error"), Exception):
                err["ctx"]["error"] = str(err["ctx"]["error"])
        return errors

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "code": 422,
            "message": "Validation failed",
            "detail": clean_errors(exc.errors()),
        },
    )


# 🧩 HTTP 예외 처리
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.status_code,
            "message": exc.detail,
        },
    )


print(f"[INFO] 현재 실행 환경: {os.getenv('ENV')}")
