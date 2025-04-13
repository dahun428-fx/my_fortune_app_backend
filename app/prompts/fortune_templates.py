from pathlib import Path


def get_fortune_prompt(language: str) -> str:
    filename = f"fortune_{language}.txt"
    path = Path("app/prompts/templates") / filename
    return path.read_text(encoding="utf-8")
