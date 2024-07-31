from typing import Optional, Type

from langchain.callbacks.manager import AsyncCallbackManagerForToolRun
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field
from rss3_dsl_sdk.client import RSS3Client
from rss3_dsl_sdk.schemas.base import ActivityFilter, PaginationOptions

from openagent.agent.system_prompt import FEED_PROMPT

SUPPORTED_NETWORKS = ["arbitrum", "avax", "base", "binance-smart-chain", "ethereum", "gnosis", "linea", "optimism", "polygon"]
DEFI_ACTIVITIES = ["swap", "liquidity", "staking"]


class ParamSchema(BaseModel):
    address: str = Field(description="Wallet address or blockchain domain name (e.g., vitalik.eth)")
    activity_type: str = Field(description=f"Type of DeFi activity. Supported types: {', '.join(DEFI_ACTIVITIES)}")
    network: Optional[str] = Field(default=None, description=f"Network for activities. Supported: {', '.join(SUPPORTED_NETWORKS)}")


class DeFiExpert(BaseTool):
    name = "DeFiExecutor"
    description = "Get insights into user's DeFi activities (swaps, liquidity provision, staking) across various networks."
    args_schema: Type[ParamSchema] = ParamSchema

    async def _arun(
        self,
        address: str,
        activity_type: str,
        network: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        if activity_type.lower() not in DEFI_ACTIVITIES:
            return f"Error: Unsupported activity type '{activity_type}'. Choose from: {', '.join(DEFI_ACTIVITIES)}"

        if network and network.lower() not in map(str.lower, SUPPORTED_NETWORKS):
            return f"Error: Unsupported network '{network}'. Choose from: {', '.join(SUPPORTED_NETWORKS)}"

        try:
            client = RSS3Client()
            filters = ActivityFilter(network=[network] if network else None)
            pagination = PaginationOptions(limit=10, action_limit=10)

            fetch_method = getattr(client, f"fetch_exchange_{activity_type.lower()}_activities")
            activities = fetch_method(account=address, filters=filters, pagination=pagination)

            if not activities.data:
                return f"No {activity_type} activities found for {address}{' on ' + network if network else ''}."

            result = FEED_PROMPT.format(activities_data=activities.dict(), activity_type=activity_type)
            return result

        except Exception as e:
            logger.error(f"Error fetching DeFi activities: {e}")
            return f"Error: Unable to fetch data. {e}"
