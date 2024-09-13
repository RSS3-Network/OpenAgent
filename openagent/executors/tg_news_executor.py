import asyncio
import json
from typing import Any, Dict, List, Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.executors.tg_util import fetch_tg_msgs


class ParamSchema(BaseModel):
    """
    Defines the schema for input parameters of the TelegramNewsExecutor tool.
    """

    limit: int = Field(default=10, description="Number of recent news items to fetch from Telegram channels")


class TelegramNewsExecutor(BaseTool):
    """
    A tool for fetching recent news from specific Telegram channels using RSS3 DATA API.
    """

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    name = "TelegramNewsExecutor"
    description = """Use this tool to get recent news and updates in the blockchain \
and cryptocurrency space."""
    args_schema: Type[ParamSchema] = ParamSchema

    async def _arun(
        self,
        limit: int = 10,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Asynchronously run the Telegram news fetching process.

        :param limit: Number of recent news items to fetch
        :param run_manager: Optional callback manager for async operations
        :return: A string containing the fetched news items
        """
        return await fetch_telegram_news(["ChannelPANews", "chainfeedsxyz"], limit)


async def fetch_telegram_news(channels: List[str], limit: int = 10) -> str:
    """
    Fetch recent news from specific Telegram channels using RSS3 DATA API.

    :param channels: List of Telegram channels to fetch news from
    :param limit: Number of recent news items to fetch
    :return: A string containing the fetched news items
    """
    results = []
    try:
        results = list(await asyncio.gather(*[fetch_tg_msgs(channel, limit) for channel in channels]))
        return format_news(results)
    except Exception as e:
        if results:
            return f"An error occurred while fetching news, this is the results: {json.dumps(results)}"
        return f"An error occurred while fetching news: {str(e)}"


def format_news(results: List[List[Dict]]) -> str:
    """
    Format the fetched news results into a readable string.

    :param results: A list of lists containing news entries
    :return: A formatted string of news items
    """
    formatted_news = [format_entry(entry) for item in results for entry in item]
    return "Recent news from Telegram channels:\n\n" + "\n".join(formatted_news)


def format_entry(entry: Dict) -> str:
    """
    Format a single news entry into a readable string.

    :param entry: A dictionary containing news entry data
    :return: A formatted string of the news entry
    """
    metadata = entry["actions"][0]["metadata"]
    return f"Title: {metadata['title']}\nDate: {metadata['pub_date']}\nSummary: {metadata['description']}\n\n"


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    entries = loop.run_until_complete(fetch_telegram_news(["ChannelPANews", "chainfeedsxyz"], 10))
    print(entries)
