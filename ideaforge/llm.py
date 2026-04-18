from langchain_nvidia_ai_endpoints import ChatNVIDIA

from .config import MODEL_ID


def get_llm(temperature: float = 0.2, max_tokens: int = 2048) -> ChatNVIDIA:
    return ChatNVIDIA(
        model=MODEL_ID,
        temperature=temperature,
        max_tokens=max_tokens,
    )
