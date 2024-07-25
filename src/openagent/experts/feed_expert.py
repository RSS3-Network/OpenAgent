from typing import Optional, Type

import aiohttp
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

from openagent.agent.system_prompt import FEED_PROMPT
from openagent.conf.env import settings


class ParamSchema(BaseModel):
    address: str = Field(
        description="""wallet address or blockchain domain name,\
hint: vitalik's address is vitalik.eth"""
    )

    type: str = Field(
        description="""Retrieve activities for the specified type,
eg. : all, post, comment, share."""
    )


class FeedExpert(BaseTool):
    name = "FeedExecutor"
    description = """Use this tool to get the activities of a wallet address or \
blockchain domain name and know what this address has done or doing recently."""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        address: str,
        type: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        address: str,
        type: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_feeds(address, type)


async def fetch_feeds(address: str, type: str):
    url = f"{settings.RSS3_DATA_API}/decentralized/{address}?limit=5&action_limit=10&tag=social"
    if type in ["post", "comment", "share"]:
        url += f"&type={type}"
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()

    result = FEED_PROMPT.format(activities_data=data)

    return result
