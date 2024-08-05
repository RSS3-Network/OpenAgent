from typing import Optional, Type

from langchain.callbacks.manager import AsyncCallbackManagerForToolRun
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field
from rss3_dsl_sdk.client import RSS3Client
from rss3_dsl_sdk.schemas.base import ActivityFilter, PaginationOptions

from openagent.executors.feed_prompt import FEED_PROMPT

# Define the defi activities and common DeFi networks
SUPPORTED_NETWORKS = ["arbitrum", "avax", "base", "binance-smart-chain", "ethereum", "gnosis", "linea", "optimism", "polygon"]
DEFI_ACTIVITIES = ["swap", "liquidity", "staking", "all"]


# Define the schema for input parameters
class ParamSchema(BaseModel):
    """
    Defines the schema for input parameters of the DeFiExecutor tool.
    """

    address: str = Field(description="Wallet address or blockchain domain name (e.g., vitalik.eth)")
    activity_type: str = Field(description=f"Type of DeFi activity. Supported types: {', '.join(DEFI_ACTIVITIES)}")
    network: Optional[str] = Field(default=None, description=f"Network for activities. Supported: {', '.join(SUPPORTED_NETWORKS)}")


class DeFiExecutor(BaseTool):
    """
    A tool for fetching and analyzing DeFi activities across various networks.
    """

    name = "DeFiExecutor"
    description = "Use this tool to get the user's DeFi activities (swaps, liquidity provision, staking, all) across various networks."
    args_schema: Type[ParamSchema] = ParamSchema

    async def _run(
        self,
        address: str,
        activity_type: str,
        network: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(self, address: str, activity_type: str, network: Optional[str] = None) -> str:
        """
        Asynchronously run the DeFi activity fetching process.

        :param address: The wallet address to fetch activities for
        :param activity_type: The type of DeFi activity to fetch, now supports "swap", "liquidity", "staking"
        :param network: network to filter activities (OPTIONAL)
        :return: A string containing the fetched DeFi activities or an error message
        """
        return await self.fetch_defi_feeds(address, network, activity_type)

    async def fetch_defi_feeds(self, address: str, network: Optional[str] = None, activity_type: Optional[str] = None):
        """
        Fetch DeFi feed activities for a given address, optionally filtered by network and activity type.

        :param address: The wallet address to fetch activities for
        :param network: network to filter activities (Optional)
        :param activity_type: The type of DeFi activity to fetch
        :return: A string containing the fetched DeFi activities or an error message
        """
        # Validate activity type
        if activity_type.lower() not in DEFI_ACTIVITIES:
            return f"Error: Unsupported activity type '{activity_type}'. Choose from: {', '.join(DEFI_ACTIVITIES)}"

        # Validate network if provided
        if network and network.lower() not in map(str.lower, SUPPORTED_NETWORKS):
            return f"Error: Unsupported network '{network}'. Choose from: {', '.join(SUPPORTED_NETWORKS)}"

        try:
            client = RSS3Client()
            filters = ActivityFilter(network=[network] if network else None)
            pagination = PaginationOptions(limit=10, action_limit=10)

            # Handle 'all' activity type
            if activity_type == "all":
                activities = []
                for act_type in ["swap", "liquidity", "staking"]:
                    fetch_method = getattr(client, f"fetch_exchange_{act_type}_activities")
                    act_results = fetch_method(account=address, filters=filters, pagination=pagination)
                    activities.extend(act_results.data)
            else:
                fetch_method = getattr(client, f"fetch_exchange_{activity_type}_activities")
                activities_result = fetch_method(account=address, filters=filters, pagination=pagination)
                activities = activities_result.data

            # Check if any activities were found
            if not activities:
                return (
                    f"No {'DeFi' if activity_type == 'all' else activity_type} activities found for {address}{' on ' + network if network else ''}."
                )

            # Format the result
            activities_data = [activity.model_dump() for activity in activities]
            result = FEED_PROMPT.format(activities_data=activities_data, activity_type="DeFi" if activity_type == "all" else activity_type)
            return result

        except Exception as e:
            logger.error(f"Error fetching DeFi activities: {e}")
            return f"Error: Unable to fetch data. {e}"
