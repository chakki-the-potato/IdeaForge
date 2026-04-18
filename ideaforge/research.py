from .config import MOCK_MODE

CATEGORIES: list[tuple[str, str]] = [
    ("competitors", "경쟁사 및 유사 서비스"),
    ("market_size", "시장 규모 및 트렌드"),
    ("target_persona", "타겟 페르소나"),
    ("real_cases", "실제 사례"),
    ("pain_points", "사용자 불편점 (Pain points)"),
]

_MOCK_TEMPLATE = (
    "(모의 모드 결과) 실제 Tavily 검색 없이 생성된 샘플입니다.\n"
    "- 이 섹션은 카테고리: **{label}** 에 해당합니다.\n"
    "- 실제 실행은 NVIDIA / Tavily API 키를 설정하고 IDEAFORGE_MOCK 을 해제한 뒤 수행하세요."
)


def run(idea: str, enriched_context: str, verbose: bool = True) -> dict[str, str]:
    """Run a ReAct agent per category. Returns {key: markdown_summary}."""
    if MOCK_MODE:
        if verbose:
            print("[mock] 모의 모드로 카테고리별 샘플 요약을 생성합니다.")
        return {key: _MOCK_TEMPLATE.format(label=label) for key, label in CATEGORIES}

    from .agent import build_research_agent
    from .prompts import RESEARCHER

    results: dict[str, str] = {}
    for key, label in CATEGORIES:
        if verbose:
            print(f"\n[리서치] {label} 조사 중...")
        agent = build_research_agent(RESEARCHER.format(category=label))
        user_msg = (
            f"조사 항목: {label}\n\n아이디어: {idea}\n\nFollow-up Q&A:\n{enriched_context}"
        )
        try:
            state = agent.invoke({"messages": [("user", user_msg)]})
            results[key] = _last_ai_text(state)
        except Exception as exc:
            results[key] = f"(이 항목 조사 중 오류 발생: {exc})"
            if verbose:
                print(f"  ! 실패: {exc}")
    return results


def _last_ai_text(state: dict) -> str:
    messages = state.get("messages", [])
    for msg in reversed(messages):
        content = getattr(msg, "content", None)
        if content and not getattr(msg, "tool_calls", None):
            return content.strip()
    return "(결과 없음)"
