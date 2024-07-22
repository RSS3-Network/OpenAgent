from typing import Optional, Type

import requests
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from langchain_community.utilities import SerpAPIWrapper
from pydantic import BaseModel, Field

from openagent.conf.env import settings


class SearchSchema(BaseModel):
    query: str = Field(description="The search query keywords.")
    search_type: str = Field(
        description="""The type of search to perform. Options are:
        - "google": Google search for current events and real-time information
        - "dune": Search for Dune dashboards"""
    )
    gl: Optional[str] = Field(
        default="us",
        description="Country code for Google search, e.g., 'us', 'cn', 'jp'",
    )
    hl: Optional[str] = Field(
        default="en",
        description="Language code for Google search, e.g., 'en', 'zh-cn', 'ja'",
    )


def dune_search(query: str) -> str:
    url = f"{settings.RSS3_SEARCH_API}/dune/search?keyword={query}"
    headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("GET", url, headers=headers)
    return response.text


def google_search(query: str, gl: str, hl: str) -> str:
    search_wrapper = SerpAPIWrapper(
        search_engine="google",
        params={"engine": "google", "gl": gl, "hl": hl},
    )
    return search_wrapper.run(query)


class SearchTool(BaseTool):
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
        gl: Optional[str] = "us",
        hl: Optional[str] = "en",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        if search_type == "google":
            return google_search(query, gl, hl)
        elif search_type == "dune":
            return dune_search(query)
        else:
            raise ValueError(f"Unknown search type: {search_type}")

    async def _arun(
        self,
        query: str,
        search_type: str,
        gl: Optional[str] = "us",
        hl: Optional[str] = "en",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        if search_type == "google":
            return google_search(query, gl, hl)
        elif search_type == "dune":
            return dune_search(query)
        else:
            raise ValueError(f"Unknown search type: {search_type}")
