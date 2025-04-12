from app.models.fortune import FortuneRequest, FortuneResponse
import httpx
import os

GROQ_API_URL = "https://api.groq.com/v1/some-endpoint"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

async def get_fortune(req: FortuneRequest) -> FortuneResponse:
    # 예시 LLM 요청
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={"prompt": f"{req.name}의 운세를 알려줘"}
        )
        data = response.json()
        return FortuneResponse(result=data.get("result", "운세 결과 없음"))
