from langchain_community.tools.tavily_search import TavilySearchResults


def get_search_tool(max_results: int = 5) -> TavilySearchResults:
    return TavilySearchResults(
        max_results=max_results,
        search_depth="advanced",
        include_answer=True,
    )
