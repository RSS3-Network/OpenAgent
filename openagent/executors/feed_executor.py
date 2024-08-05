from typing import Optional, Type

import aiohttp
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

from openagent.conf.env import settings
from openagent.executors.feed_prompt import FEED_PROMPT


class ParamSchema(BaseModel):
    """
    Defines the schema for input parameters of the FeedExecutor tool.
    """

    address: str = Field(
        description="""wallet address or blockchain domain name,\
hint: vitalik's address is vitalik.eth"""
    )

    type: str = Field(
        description="""Retrieve activities for the specified type,
eg. : all, post, comment, share."""
    )


class FeedExecutor(BaseTool):
    """
    A tool for fetching and analyzing blockchain activities for a given address.
    """

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
        """
        Asynchronously run the feed fetching process.

        :param address: The wallet address to fetch activities for
        :param type: The type of activities to fetch (all, post, comment, share)
        :param run_manager: Optional callback manager for async operations
        :return: A string containing the fetched activities or an error message
        """
        return await fetch_feeds(address, type)


async def fetch_feeds(address: str, type: str):
    """
    Fetch feed activities for a given address and activity type.

    :param address: The wallet address to fetch activities for
    :param type: The type of activities to fetch (all, post, comment, share)
    :return: A string containing the fetched activities formatted using FEED_PROMPT
    """

    # Construct the URL for the API request
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
