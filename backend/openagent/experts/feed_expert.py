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
    address: str = Field(
        description="""wallet address or blockchain domain name,\
hint: vitalik's address is vitalik.eth"""
    )
    platform: str = Field(
        description="platform filter, default is '', option: lens, mirror, uniswap.",
        default="",
    )


class FeedExpert(BaseTool):
    name = "feed"
    description = """Use this tool to get the activities of a wallet address or \
blockchain domain name on a platform, and know
 what this address has done or doing recently."""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        address: str,
        platform: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        address: str,
        platform: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_feeds(address, platform)


async def fetch_feeds(address: str, platform: str):
    host = "https://api.rss3.io/v1/notes/"
    url = f"""{host}{address}?limit=5&platform={platform}"""
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
        async with session.get(url, headers=headers) as resp:
            return await resp.text()
