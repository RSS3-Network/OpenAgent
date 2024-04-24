from datetime import datetime
from typing import Optional, Type

import aiohttp
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field


class ParamSchema(BaseModel):
    query: str = Field(description="should be a search query")
    platform: str = Field(
        description="""platform filter, default platform is "", \
other option: "farcaster", "lens", "mastodon", "matters", "mirror", "xlog"."""
    )


class HootExpert(BaseTool):
    name = "hoot"
    description = """useful for when you need to search some posts or articles \
on farcaster, lens, mastodon, matters, mirror, xlog."""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        query: str,
        platform: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        query: str,
        platform: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_articles(query, platform)


async def fetch_articles(query: str, platform: str):
    host = "https://testnet.rss3.io/search/activities?"
    params = f"keyword={query}&offset=0&limit=5&platform={platform}"
    url = f"{host}{params}"
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
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
            return articles
