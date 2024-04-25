import json
from datetime import datetime
from typing import Optional, Type

import aiohttp
import requests
from langchain import SerpAPIWrapper
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field


class SearchSchema(BaseModel):
    query: str = Field(description="The search query keywords.")
    search_type: str = Field(
        description="""The type of search to perform. Options are:
        - "google": Google search for current events and real-time information
        - "hoot": Search for posts or articles on various platforms
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
    platform: Optional[str] = Field(
        default="",
        description="""Platform filter for Hoot search. Default is "".
        Other options: "farcaster", "lens", "mastodon", "matters", "mirror", "xlog".""",
    )


class SearchExpert(BaseTool):
    name = "search"
    description = """
    A versatile search tool that can perform various types of searches based on the query type:
    - For queries related to charts, data visualization, or dashboards, use Dune search.
    - For queries about project introductions, current events or real-time information, use Google search.
    - For queries seeking articles or posts on various platforms, use Hoot search."""  # noqa: E501
    args_schema: Type[SearchSchema] = SearchSchema

    def _run(
        self,
        query: str,
        search_type: str,
        gl: Optional[str] = "us",
        hl: Optional[str] = "en",
        platform: Optional[str] = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        query: str,
        search_type: str,
        gl: Optional[str] = "us",
        hl: Optional[str] = "en",
        platform: Optional[str] = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        if search_type == "google":
            return await self.google_search(query, gl, hl)
        elif search_type == "hoot":
            return await self.hoot_search(query, platform)
        elif search_type == "dune":
            return await self.dune_search(query)
        else:
            raise ValueError(f"Unknown search type: {search_type}")

    async def google_search(self, query: str, gl: str, hl: str) -> str:
        search_wrapper = SerpAPIWrapper(
            search_engine="google",
            params={"engine": "google", "gl": gl, "hl": hl},
        )
        return search_wrapper.run(query)

    async def hoot_search(self, query: str, platform: str) -> str:
        host = "https://testnet.rss3.io/search/activities?"
        params = f"keyword={query}&offset=0&limit=5&platform={platform}"
        url = f"{host}{params}"
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession() as session:
            logger.info(f"Fetching {url}")
            async with session.get(url, headers=headers) as resp:
                result = await resp.json()
                articles = []
                for doc in result["data"]["docs"]:
                    timestamp = doc["timestamp"]
                    readable_time = datetime.fromtimestamp(timestamp / 1000).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    article = {
                        "title": doc["actions"][0]["search_extension"]["highlighting"][
                            "title"
                        ],
                        "media": doc["actions"][0]["search_extension"]["media"],
                        "author": doc["actions"][0]["search_extension"]["author"],
                        "body": doc["actions"][0]["search_extension"]["highlighting"][
                            "body"
                        ],
                        "url": doc["actions"][0]["related_urls"][0],
                        "platform": doc["platform"],
                        "timestamp": readable_time,
                    }
                    articles.append(article)
                return json.dumps(articles)

    async def dune_search(self, query: str) -> str:
        url = f"https://devnet.rss3.io/search/dune/search?keyword={query}"
        headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        response = requests.request("GET", url, headers=headers)
        return response.text
