from langchain_community.tools.tavily_search import TavilySearchResults

tavily_executor = TavilySearchResults(max_results=5, name="SearchExecutor")
