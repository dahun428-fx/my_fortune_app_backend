# app/utils/clean.py


def clean_fortune_result(text: str, name: str | None, language: str = "ko") -> str:
    if not text or text.lower() in ["none", "null"]:
        return (
            "운세 정보를 가져오지 못했습니다. 다시 시도해 주세요."
            if language == "ko"
            else "Failed to retrieve your fortune. Please try again."
        )

    # 이름이 None일 경우 대체
    if name is None or name.strip() == "":
        text = text.replace("None", "당신" if language == "ko" else "you")

    return text.strip()
