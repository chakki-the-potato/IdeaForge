"""IdeaForge CLI entrypoint.

Usage:
    python main.py                      # interactive one-line idea input
    python main.py examples/sketch.md   # load multi-paragraph sketch from file
"""

from __future__ import annotations

import sys
from pathlib import Path

from ideaforge import construct, interview, report, research
from ideaforge.config import MOCK_MODE


def _prompt(text: str) -> str:
    try:
        return input(text).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n중단되었습니다.")
        sys.exit(130)


def _load_sketch() -> str:
    if len(sys.argv) >= 2:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"파일을 찾을 수 없습니다: {path}")
            sys.exit(1)
        return path.read_text(encoding="utf-8").strip()
    return _prompt("아이디어를 한 줄로 입력하세요:\n> ")


def main() -> None:
    print("=" * 60)
    print("IdeaForge — AI-Powered Idea Research Agent")
    print("Powered by NVIDIA NIM (Nemotron) + LangGraph + Tavily")
    if MOCK_MODE:
        print("** MOCK MODE: API 호출 없이 샘플 결과로 플로우만 시연합니다 **")
    print("=" * 60)

    sketch = _load_sketch()
    if not sketch:
        print("입력이 비어 있습니다. 종료합니다.")
        return

    print("\n[1/4] follow-up 질문 생성 중...")
    questions = interview.generate_followups(sketch)

    print("\n[2/4] 맥락 보완을 위해 3가지 질문에 답해주세요.")
    answers: list[str] = []
    for i, question in enumerate(questions, start=1):
        print(f"\nQ{i}. {question}")
        answers.append(_prompt("A: "))

    enriched = interview.compose_context(questions, answers)

    print("\n[3/4] 웹 리서치 실행 (카테고리 5개, 약 1~3분 소요)...")
    research_results = research.run(sketch, enriched, verbose=True)

    print("\n[4/4] 제품 구성 생성 중 (개요 / 시나리오 / 로드맵 / 위험)...")
    overview = construct.generate_overview(sketch, enriched, research_results)
    scenarios = construct.generate_scenarios(sketch, enriched, research_results)
    roadmap = construct.generate_roadmap(sketch, enriched, research_results)
    risks = construct.generate_risks(sketch, enriched, research_results)

    markdown = report.render(
        sketch,
        enriched,
        research_results,
        overview=overview,
        scenarios=scenarios,
        roadmap=roadmap,
        risks=risks,
    )
    path = report.save(markdown, sketch)

    print("\n" + "=" * 60)
    print(f"리포트 저장 완료: {path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
