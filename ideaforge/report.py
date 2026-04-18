import re
from datetime import datetime
from pathlib import Path

from .config import MODEL_ID, OUTPUT_DIR
from .research import CATEGORIES

_SLUG_PATTERN = re.compile(r"[^0-9A-Za-z가-힣]+")


def render(
    sketch: str,
    enriched_context: str,
    research_results: dict[str, str],
    *,
    overview: str,
    scenarios: str,
    roadmap: str,
    risks: str,
) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = [
        "# IdeaForge 리서치 리포트",
        "",
        f"- 생성 시각: {timestamp}",
        f"- 모델: `{MODEL_ID}`",
        "",
        "## 아이디어 / 스케치",
        "",
        sketch.strip(),
        "",
        "## Follow-up Q&A",
        "",
        enriched_context.strip() or "(답변 없음)",
        "",
        "## 제품 개요",
        "",
        overview.strip(),
        "",
        "## 사용자 시나리오",
        "",
        scenarios.strip(),
        "",
        "## MVP 로드맵",
        "",
        roadmap.strip(),
        "",
        "## 위험 및 가정",
        "",
        risks.strip(),
        "",
        "## 리서치 결과",
        "",
    ]
    for key, label in CATEGORIES:
        summary = research_results.get(key, "(결과 없음)").strip()
        lines.append(f"### {label}")
        lines.append("")
        lines.append(summary)
        lines.append("")
    return "\n".join(lines)


def save(markdown: str, sketch: str, output_dir: Path = OUTPUT_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{stamp}_{_slugify(sketch)}.md"
    path.write_text(markdown, encoding="utf-8")
    return path


def _slugify(text: str, max_len: int = 40) -> str:
    first_line = next((line for line in text.splitlines() if line.strip()), text)
    first_line = first_line.lstrip("#").strip()
    slug = _SLUG_PATTERN.sub("-", first_line).strip("-")
    return (slug[:max_len] or "idea").lower()
