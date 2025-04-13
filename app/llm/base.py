# app/llm/base.py
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass
