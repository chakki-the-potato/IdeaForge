from langgraph.prebuilt import create_react_agent

from .llm import get_llm
from .tools import get_search_tool


def build_research_agent(system_prompt: str, max_results: int = 5):
    return create_react_agent(
        model=get_llm(),
        tools=[get_search_tool(max_results=max_results)],
        prompt=system_prompt,
    )
