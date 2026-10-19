import os
from langchain_openai import ChatOpenAI
from .config import settings


def get_llm(temperature: float = 0.0):
    if settings.mode == "offline":
        return None
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required unless SIFT_MODE=offline")
    return ChatOpenAI(model=settings.model, temperature=temperature)
