import logging
from app.chain.groq_chain import get_fortune_llm_answer
from app.models.fortune import FortuneRequest, FortuneResponse
from app.prompts.fortune_templates import get_fortune_prompt
from app.utils.clean import clean_fortune_result  # 후처리 함수

logger = logging.getLogger(__name__)


def map_calendar_type(calendar_type: str, language: str) -> str:
    if language == "ko":
        return "양력" if calendar_type == "solar" else "음력"
    return calendar_type  # e.g., 'solar' or 'lunar'


def map_gender(gender: str, language: str) -> str:
    if language == "en":
        return "남성" if gender == "male" else "여성"
    return gender


def map_topic_to_korean(topic: str, language: str) -> str:
    if language == "ko":
        mapping = {
            "romance": "연애운",
            "money": "금전운",
            "health": "건강운",
            "career": "직장운",
            "daily": "오늘의 한 줄 운세",
            "general fortune": "종합 운세",
        }
        return mapping.get(topic, topic)
    return topic


async def get_fortune(req: FortuneRequest) -> FortuneResponse:
    logger.info("[요청 데이터] %s", req.model_dump())

    # 다국어 → 한글 변환 처리
    gender = map_gender(req.gender, req.language)
    calendar_type = map_calendar_type(req.calendar_type, req.language)
    topic_raw = req.topic or (
        "종합 운세" if req.language == "ko" else "general fortune"
    )
    topic_kor = map_topic_to_korean(topic_raw, req.language)

    # 템플릿 적용
    prompt_template = get_fortune_prompt(language=req.language)
    prompt = prompt_template.format(
        name=req.name or "",
        gender=gender,
        birth=req.birth,
        birth_time=req.birth_time or "",
        calendar_type=calendar_type,
        topic=topic_kor,
    )

    logger.debug("[생성된 프롬프트]:\n%s", prompt)

    try:
        result = get_fortune_llm_answer(prompt)
        cleaned_result = clean_fortune_result(result, req.name, req.language)
        logger.info("[LLM 응답]: %s", cleaned_result)
        return FortuneResponse(result=cleaned_result)

    except Exception as e:
        logger.exception("운세 생성 중 오류 발생")
        fallback = (
            "운세 정보를 생성하지 못했습니다. 다시 시도해주세요."
            if req.language == "ko"
            else "Unable to generate your fortune at this time."
        )
        return FortuneResponse(result=fallback)
