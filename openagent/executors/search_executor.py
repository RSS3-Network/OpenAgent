from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults

from openagent.conf.env import settings


class SearchExecutor:
    def __new__(cls):
        if settings.TAVILY_API_KEY:
            return TavilySearchResults(max_results=5, name="TavilySearchExecutor")
        else:
            return DuckDuckGoSearchRun(name="DuckDuckGoSearchExecutor")


search_executor = SearchExecutor()
