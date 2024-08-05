from typing import Optional, Type

import requests
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.conf.env import settings


class NFTRankingArgs(BaseModel):
    sort_field: str = Field(
        default="market_cap",
        description="""
Options include: volume_1d, volume_7d, volume_30d, volume_total, volume_change_1d,
volume_change_7d, volume_change_30d, sales_1d, sales_7d, sales_30d,
sales_total, sales_change_1d, sales_change_7d, sales_change_30d,
floor_price, market_cap.
    """,
    )


class NFTRankingExecutor(BaseTool):
    name = "NFTRankingExecutor"
    description = "A tool for getting NFT collection rankings."
    args_schema: Type[NFTRankingArgs] = NFTRankingArgs

    def _run(
        self,
        sort_field: str = "market_cap",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.collection_ranking(sort_field)

    async def _arun(
        self,
        sort_field: str = "market_cap",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return self._run(sort_field, run_manager)

    @staticmethod
    def collection_ranking(sort_field: str) -> str:
        """Search for NFT collections ranking."""
        url = f"https://restapi.nftscan.com/api/v2/statistics/ranking/collection?sort_field={sort_field}&sort_direction=desc&limit=20"

        headers = {"X-API-KEY": f"{settings.NFTSCAN_API_KEY}"}
        response = requests.get(url, headers=headers)
        return response.text
