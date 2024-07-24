from typing import Optional, Type

import requests
from langchain import SerpAPIWrapper
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.conf.env import settings


class SearchSchema(BaseModel):
    query: str = Field(description="The search query keywords.")
    search_type: str = Field(
        description="""The type of search to perform. Options are:
        - "google": Google search for current events and real-time information
        - "dune": Search for Dune dashboards"""
    )


async def dune_search(query: str) -> str:
    url = f"{settings.RSS3_SEARCH_API}/dune/search?keyword={query}"
    headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("GET", url, headers=headers)
    return response.text


async def google_search(query: str) -> str:
    search_wrapper = SerpAPIWrapper(
        search_engine="google",
        params={"engine": "google"},
    )
    return search_wrapper.run(query)


class SearchExpert(BaseTool):
    name = "search"
    description = """
    A versatile search tool that can perform various types of searches based on the query type:
    - For queries related to charts, data visualization, or dashboards, use Dune search.
    - For queries about project introductions, current events or real-time information, use Google search."""
    args_schema: Type[SearchSchema] = SearchSchema

    def _run(
        self,
        query: str,
        search_type: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        query: str,
        search_type: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        if search_type == "google":
            return await google_search(query)
        elif search_type == "dune":
            return await dune_search(query)
        else:
            raise ValueError(f"Unknown search type: {search_type}")
