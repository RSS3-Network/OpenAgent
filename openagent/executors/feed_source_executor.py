from typing import Optional, Type

from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field
from rss3_dsl_sdk.client import RSS3Client
from rss3_dsl_sdk.schemas.base import ActivityFilter, PaginationOptions

from openagent.executors.feed_prompt import FEED_PROMPT

# Define supported networks and platforms
SUPPORTED_NETWORKS = [
    "arbitrum",
    "arweave",
    "avax",
    "base",
    "binance-smart-chain",
    "crossbell",
    "ethereum",
    "farcaster",
    "gnosis",
    "linea",
    "optimism",
    "polygon",
    "vsl",
]

ALLOWED_PLATFORMS = [
    "1inch",
    "AAVE",
    "Aavegotchi",
    "Crossbell",
    "Curve",
    "ENS",
    "Farcaster",
    "Highlight",
    "IQWiki",
    "KiwiStand",
    "Lens",
    "Lido",
    "LooksRare",
    "Matters",
    "Mirror",
    "OpenSea",
    "Optimism",
    "Paragraph",
    "RSS3",
    "SAVM",
    "Stargate",
    "Uniswap",
    "Unknown",
    "VSL",
]


# Define the schema for input parameters
class ParamSchema(BaseModel):
    address: str = Field(
        description="""wallet address or blockchain domain name,\
hint: vitalik's address is vitalik.eth"""
    )

    network: Optional[str] = Field(
        default=None,
        description=f"""Retrieve activities for the specified network.
Supported networks: {', '.join(SUPPORTED_NETWORKS)}""",
    )

    platform: Optional[str] = Field(
        default=None,
        description=f"""Retrieve activities for the specified platform.
Allowed platforms: {', '.join(ALLOWED_PLATFORMS)}""",
    )


# Define the FeedSourceExecutor tool
class FeedSourceExecutor(BaseTool):
    name = "FeedSourceExecutor"
    description = """Use this tool to get the activities of a wallet address or \
blockchain domain name based on specific network and/or platform, and know what this address \
has done or is doing recently."""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        address: str,
        network: Optional[str] = None,
        platform: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        address: str,
        network: Optional[str] = None,
        platform: Optional[str] = None,
    ):
        """
        Asynchronously run the feed source fetching process.

        :param address: The wallet address to fetch activities for
        :param network: network to filter activities (Optional)
        :param platform: platform to filter activities (Optional)
        :return: A string containing the fetched activities or an error message
        """
        return await self.fetch_source_feeds(address, network, platform)

    async def fetch_source_feeds(self, address: str, network: Optional[str] = None, platform: Optional[str] = None):
        """
        Fetch feed activities for a given address, optionally filtered by network and platform.
        """
        filters = ActivityFilter()
        pagination = PaginationOptions(limit=5, action_limit=10)

        # Validate and set network and platform filter if provided
        if network:
            if network.lower() not in [n.lower() for n in SUPPORTED_NETWORKS]:
                return f"Error: Unsupported network '{network}'. Please choose from: {', '.join(SUPPORTED_NETWORKS)}"
            filters.network = [network]

        if platform:
            if platform.lower() not in [p.lower() for p in ALLOWED_PLATFORMS]:
                return f"Error: Unsupported platform '{platform}'. Please choose from: {', '.join(ALLOWED_PLATFORMS)}"
            filters.platform = [platform]

        try:
            logger.info(f"Fetching activities for address: {address}, network: {network}, platform: {platform}")

            # Fetch activities using the RSS3 client
            activities = RSS3Client().fetch_activities(account=address, tag=None, activity_type=None, pagination=filters, filters=pagination)

            # Check if any activities were found
            if not activities.data:
                return f"No activities found for the given address{' on ' + network if network else ''}{' and ' + platform if platform else ''}."

            result = FEED_PROMPT.format(activities_data=activities.dict())
            return result

        except Exception as e:
            logger.error(f"Error fetching activities: {e!s}")
            return f"Error: Unable to fetch data. {e!s}"
