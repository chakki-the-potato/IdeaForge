import re

from .config import MOCK_MODE

_LINE_PATTERN = re.compile(r"^\s*\d+[.)\]]\s*(.+?)\s*$")

_MOCK_QUESTIONS = [
    "타겟 사용자 그룹과 대표적인 사용 시나리오는 무엇인가요?",
    "수익 모델과 예상 가격 구조는 어떻게 설계되어 있나요?",
    "기존 대안 대비 가장 강력한 차별화 포인트 한 가지는 무엇인가요?",
]


def generate_followups(idea: str, n: int = 3) -> list[str]:
    """Ask Nemotron to produce exactly `n` follow-up questions in Korean."""
    if MOCK_MODE:
        return _MOCK_QUESTIONS[:n]

    from langchain_core.messages import HumanMessage, SystemMessage

    from .llm import get_llm
    from .prompts import INTERVIEWER

    llm = get_llm(temperature=0.3, max_tokens=512)
    response = llm.invoke(
        [
            SystemMessage(content=INTERVIEWER),
            HumanMessage(content=f"아이디어: {idea}"),
        ]
    )
    questions = _parse_numbered_list(response.content)
    if len(questions) < n:
        raise RuntimeError(
            f"LLM이 요구된 {n}개의 follow-up 질문을 생성하지 못했습니다.\n원문: {response.content}"
        )
    return questions[:n]


def _parse_numbered_list(text: str) -> list[str]:
    questions: list[str] = []
    for line in text.splitlines():
        match = _LINE_PATTERN.match(line)
        if match:
            questions.append(match.group(1).strip())
    return questions


def compose_context(questions: list[str], answers: list[str]) -> str:
    """Format Q/A pairs as Markdown bullets for the report and LLM context."""
    lines: list[str] = []
    for q, a in zip(questions, answers):
        lines.append(f"- Q: {q}")
        lines.append(f"  A: {a.strip() or '(답변 없음)'}")
    return "\n".join(lines)
