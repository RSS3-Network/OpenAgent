import json

import aiohttp
from loguru import logger

from openagent.conf.env import settings


async def fetch_tg_msgs(channel: str, limit: int = 10):
    """
    Fetch recent content from a specific Telegram channel using RSS3 DATA API.

    :param channel: The Telegram channel to fetch content from
    :param limit: Number of recent items to fetch
    :return: A string containing the fetched items
    """

    url = f"{settings.RSS3_DATA_API}/rss/telegram/channel/{channel}"
    logger.info(f"Fetching content from {url}")

    async with aiohttp.ClientSession() as session:  # noqa
        async with session.get(url) as resp:
            if resp.status == 200:
                content = await resp.text()
                data = json.loads(content)
                return data["data"][:limit]
            else:
                logger.error(f"Failed to fetch from {url}. Status: {resp.status}")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    entries = loop.run_until_complete(fetch_tg_msgs("ChannelPANews", 5))
    print(entries)
