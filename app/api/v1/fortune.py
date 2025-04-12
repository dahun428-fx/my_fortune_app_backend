from fastapi import APIRouter
from app.models.fortune import FortuneRequest, FortuneResponse
from app.services.fortune_service import get_fortune

router = APIRouter()

@router.post("/fortune", response_model=FortuneResponse)
async def fortune_endpoint(req: FortuneRequest):
    return await get_fortune(req)
