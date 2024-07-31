from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

from openagent.agent.system_prompt import FEED_PROMPT
from rss3_dsl_sdk.schemas.base import PaginationOptions, ActivityFilter
from rss3_dsl_sdk.client import RSS3Client

SUPPORTED_NETWORKS = [
    "arbitrum", "avax", "base", "binance-smart-chain", "ethereum", "gnosis",
    "linea", "optimism", "polygon"
]

DEFI_ACTIVITIES = ["swap", "liquidity", "staking"]

class ParamSchema(BaseModel):
    address: str = Field(
        description="""wallet address or blockchain domain name,\
hint: vitalik's address is vitalik.eth"""
    )

    activity_type: str = Field(
        description=f"""Type of DeFi activity. 
Supported types: {', '.join(DEFI_ACTIVITIES)}"""
    )

    network: Optional[str] = Field(
        default=None,
        description=f"""Retrieve activities for the specified network. 
Supported networks: {', '.join(SUPPORTED_NETWORKS)}"""
    )

class DeFiExpert(BaseTool):
    name = "DeFiExecutor"
    description = """Use this tool to get insights into a user's DeFi activities \
such as swaps, liquidity provision, and staking across various networks."""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        address: str,
        activity_type: str,
        network: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        address: str,
        activity_type: str,
        network: Optional[str] = None,
    ):
        return await self.fetch_defi_activities(address, activity_type, network)

    async def fetch_defi_activities(self, address: str, activity_type: str, network: Optional[str] = None):
        if activity_type.lower() not in DEFI_ACTIVITIES:
            return f"Error: Unsupported activity type '{activity_type}'. Please choose from: {', '.join(DEFI_ACTIVITIES)}"

        filters = ActivityFilter()
        pagination = PaginationOptions(limit=10, action_limit=10)

        if network:
            if network.lower() not in [n.lower() for n in SUPPORTED_NETWORKS]:
                return f"Error: Unsupported network '{network}'. Please choose from: {', '.join(SUPPORTED_NETWORKS)}"
            filters.network = [network]

        try:
            logger.info(f"Fetching DeFi activities for address: {address}, activity type: {activity_type}, network: {network}")

            client = RSS3Client()

            if activity_type == "swap":
                activities = client.fetch_exchange_swap_activities(account=address, filters=filters, pagination=pagination)
            elif activity_type == "liquidity":
                activities = client.fetch_exchange_liquidity_activities(account=address, filters=filters, pagination=pagination)
            elif activity_type == "staking":
                activities = client.fetch_exchange_staking_activities(account=address, filters=filters, pagination=pagination)

            if not activities.data:
                return f"No {activity_type} activities found for the given address{' on ' + network if network else ''}."

            result = FEED_PROMPT.format(activities_data=activities.dict(), activity_type=activity_type)
            return result

        except Exception as e:
            logger.error(f"Error fetching DeFi activities: {str(e)}")
            return f"Error: Unable to fetch data. {str(e)}"