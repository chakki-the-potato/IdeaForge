"""Product construction: synthesize overview / scenarios / roadmap / risks.

Each function takes the raw sketch, follow-up Q&A, and research results, then
calls Nemotron (no web search) to produce a Markdown-formatted section.
"""

from .config import MOCK_MODE
from .research import CATEGORIES


def generate_overview(sketch: str, enriched_qa: str, research: dict[str, str]) -> str:
    if MOCK_MODE:
        return _MOCK_OVERVIEW
    from . import prompts

    return _invoke(prompts.OVERVIEW, _pack_context(sketch, enriched_qa, research))


def generate_scenarios(sketch: str, enriched_qa: str, research: dict[str, str]) -> str:
    if MOCK_MODE:
        return _MOCK_SCENARIOS
    from . import prompts

    return _invoke(prompts.SCENARIOS, _pack_context(sketch, enriched_qa, research))


def generate_roadmap(sketch: str, enriched_qa: str, research: dict[str, str]) -> str:
    if MOCK_MODE:
        return _MOCK_ROADMAP
    from . import prompts

    return _invoke(prompts.ROADMAP, _pack_context(sketch, enriched_qa, research))


def generate_risks(sketch: str, enriched_qa: str, research: dict[str, str]) -> str:
    if MOCK_MODE:
        return _MOCK_RISKS
    from . import prompts

    return _invoke(prompts.RISKS, _pack_context(sketch, enriched_qa, research))


def _invoke(system_prompt: str, user_msg: str, max_tokens: int = 3072) -> str:
    from langchain_core.messages import HumanMessage, SystemMessage

    from .llm import get_llm

    llm = get_llm(temperature=0.3, max_tokens=max_tokens)
    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_msg)]
    )
    return response.content.strip()


def _pack_context(sketch: str, enriched_qa: str, research: dict[str, str]) -> str:
    lines = [
        "# 아이디어 스케치",
        sketch.strip(),
        "",
        "# Follow-up Q&A",
        enriched_qa.strip() or "(없음)",
        "",
        "# 리서치 요약",
    ]
    for key, label in CATEGORIES:
        body = research.get(key, "").strip() or "(없음)"
        lines.append("")
        lines.append(f"## {label}")
        lines.append(body)
    return "\n".join(lines)


_MOCK_OVERVIEW = """### 문제
(모의 모드) 1인 가구가 장본 재료를 낭비하는 문제를 다룹니다. 실제 리서치 결과 연동 시 더 구체적인 숫자와 근거가 포함됩니다.

### 해결
(모의 모드) 냉장고 사진 → AI 재료 인식 → 가능 요리 추천의 세 단계로 사용자 결정 피로를 제거합니다.

### 고유 가치 제안
(모의 모드) 기존 레시피 앱 대비 "내 재료 기준"에서 출발한다는 점이 차별점입니다.
"""

_MOCK_SCENARIOS = """### 페르소나 A — 김지현, 28, 신입 개발자
- 핵심 니즈: 퇴근 후 20분 내 요리 완성
- 주된 pain point: 냉장고 속 재료를 잊고 배달로 떼움

**시나리오**
1. 트리거 상황: 금요일 저녁 귀가, 배달 피로감
2. 현재 대안의 한계: 레시피 블로그는 재료 리스트부터 요구
3. 이 제품 사용 흐름: 앱 실행 → 냉장고 촬영 → 추천 3개 → 레시피 선택 → 조리
4. 성공 기준: 사지 않은 재료 없이 20분 안에 밥상 완성

### 페르소나 B — (모의 모드 샘플)
### 페르소나 C — (모의 모드 샘플)
"""

_MOCK_ROADMAP = """### Must (MVP 핵심)
- **재료 인식**: 냉장고 사진에서 주요 재료 자동 인식.
- **요리 추천**: 인식 재료로 만들 수 있는 요리 3~5개 제안.
- **레시피 상세**: 단계별 조리법 + 소요시간 표시.
- **부족 재료 안내**: 필요하지만 없는 재료 하이라이트.
- **조리 난이도 필터**: 초보/중급/고급 선택.

### Nice (MVP 이후 경쟁 우위용)
- **쿠팡 장바구니 연동**: 부족 재료 → 커머스 제휴 (모의)
- **식단 계획**: 주간 식단 자동 구성.

### Later (장기 고려)
- **영양 분석**: 하루/주간 영양 균형 피드백.
- **커뮤니티**: 사용자 레시피 공유.
"""

_MOCK_RISKS = """1. **가정**: (사용자 행동) 사용자가 요리 전에 앱을 켤 만큼 동기가 있다.
   - **검증 방법**: 타겟 10명 주 2회 프로토타입 사용 일지.
   - **예상 비용/시간**: 2주 / 0원.

2. **가정**: (기술) 스마트폰 카메라 사진만으로 재료 인식 정확도 80% 가능.
   - **검증 방법**: 오픈소스 비전 모델 3종 벤치마크.
   - **예상 비용/시간**: 1주 / 0원.

3. **가정**: (비즈니스) 월 4,900원을 지불할 사용자 비율이 3% 이상.
   - **검증 방법**: 랜딩 페이지 + 페이월 pre-sale 실험.
   - **예상 비용/시간**: 2주 / 30만원.

(모의 모드 — 실제 실행 시 6~10개로 확장)
"""
