from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.v1 import fortune
from starlette.exceptions import HTTPException as StarletteHTTPException

# app/main.py
from app.core.logging_config import setup_logger

setup_logger()

app = FastAPI()

app.include_router(fortune.router, prefix="/api/v1")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    def clean_errors(errors):
        # ValueError 객체를 문자열로 변환
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
