from pydantic import BaseModel

class FortuneRequest(BaseModel):
    name: str
    gender: str
    birth: str
    birth_time: str
    calendar_type: str
    topic: str

class FortuneResponse(BaseModel):
    result: str
