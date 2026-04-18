import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def _truthy(value: str) -> bool:
    return value.strip().lower() in ("1", "true", "yes", "on")


MOCK_MODE: bool = _truthy(os.getenv("IDEAFORGE_MOCK", ""))


def _require(key: str) -> str:
    value = os.environ.get(key, "").strip()
    if not value:
        raise RuntimeError(
            f"환경변수 {key} 가 비어 있습니다. 프로젝트 루트의 .env 파일을 확인하세요.\n"
            f"(API 키 없이 플로우만 확인하려면 IDEAFORGE_MOCK=1 로 실행하세요)"
        )
    return value


if MOCK_MODE:
    NVIDIA_API_KEY = ""
    TAVILY_API_KEY = ""
else:
    NVIDIA_API_KEY = _require("NVIDIA_API_KEY")
    TAVILY_API_KEY = _require("TAVILY_API_KEY")

MODEL_ID: str = os.getenv(
    "NEMOTRON_MODEL_ID", "nvidia/llama-3.3-nemotron-super-49b-v1"
)
OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "outputs"))
