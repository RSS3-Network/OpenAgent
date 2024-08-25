import json
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


class ParamSchema(BaseModel):
    """
    Defines the schema for input parameters of the TelegramNewsExecutor tool.
    """

    limit: int = Field(default=10, description="Number of recent news items to fetch from Telegram channels")


class TelegramNewsExecutor(BaseTool):
    """
    A tool for fetching recent news from specific Telegram channels using RSS3 DATA API.
    """

    name = "TelegramNewsExecutor"
    description = """Use this tool to get recent news and updates in the blockchain \
and cryptocurrency space."""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        limit: int = 10,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        limit: int = 10,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        """
        Asynchronously run the Telegram news fetching process.

        :param limit: Number of recent news items to fetch
        :param run_manager: Optional callback manager for async operations
        :return: A string containing the fetched news items
        """
        return await fetch_telegram_news(limit)


async def fetch_telegram_news(limit: int = 10):
    """
    Fetch recent news from specific Telegram channels using RSS3 DATA API.

    :param limit: Number of recent news items to fetch
    :return: A string containing the fetched news items
    """
    channels = ["ChannelPANews", "chainfeedsxyz"]
    all_news = []

    async with aiohttp.ClientSession() as session:
        for channel in channels:
            url = f"{settings.RSS3_DATA_API}/rss/telegram/channel/{channel}"
            logger.info(f"Fetching news from {url}")

            async with session.get(url) as resp:
                if resp.status == 200:
                    content = await resp.text()
                    data = json.loads(content)
                    entries = data["data"][:limit]
                    all_news.extend(entries)
                else:
                    logger.error(f"Failed to fetch from {url}. Status: {resp.status}")

    formatted_news = []
    for entry in all_news:
        metadata = entry["actions"][0]["metadata"]
        formatted_entry = f"Title: {metadata['title']}\nDate: {metadata['pub_date']}\nSummary: {metadata['description']}\n\n"
        formatted_news.append(formatted_entry)

    result = "Recent news from Telegram channels:\n\n" + "\n".join(formatted_news)

    return result
