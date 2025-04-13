from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum
import re


class CalendarType(str, Enum):
    solar = "solar"
    lunar = "lunar"


class FortuneRequest(BaseModel):
    name: str | None = None
    gender: str
    birth: str
    birth_time: str | None = None
    calendar_type: CalendarType = CalendarType.solar
    topic: str | None = None
    language: str = "ko"

    @field_validator("birth")
    @classmethod
    def validate_birth_format(cls, v):
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("birth must be in YYYY-MM-DD format")
        return v

    @field_validator("birth_time")
    @classmethod
    def validate_birth_time(cls, v):
        if not v:
            return v  # allow None or ""
        try:
            datetime.strptime(v, "%H:%M")
        except ValueError:
            raise ValueError("birth_time must be in HH:MM format")
        return v

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        valid = ["남성", "여성", "male", "female"]
        if v not in valid:
            raise ValueError(
                "gender must be one of '남성', '여성', 'male', or 'female'"
            )
        return v

    @field_validator("language")
    @classmethod
    def validate_language(cls, v):
        if v not in ["ko", "en"]:
            raise ValueError("language must be either 'ko' or 'en'")
        return v


class FortuneResponse(BaseModel):
    result: str

    @property
    def cleaned_result(self) -> str:
        cleaned = self.result

        # Replace None or "null" mentions
        cleaned = re.sub(r"(사용자 이름: )None", r"\1알 수 없음", cleaned)
        cleaned = re.sub(r"(출생 시각: )None", r"\1알 수 없음", cleaned)
        cleaned = cleaned.replace("None", "")
        cleaned = cleaned.replace("null", "")

        # Remove repeated disclaimers or empty lines
        cleaned = re.sub(r"\n{2,}", "\n", cleaned)
        cleaned = cleaned.strip()
        return cleaned
