import json
from typing import Optional, Type

import requests
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.conf.env import settings


class ARGS(BaseModel):
    action: str = Field(
        description="Specify the operation to perform: 'search' for NFT "
        "collection search, 'rank' for collection ranking"
    )
    keyword: Optional[str] = Field(
        default=None,
        description="NFT symbol or collection name, required only for 'action=search'",
    )
    sort_field: Optional[str] = Field(
        default="market_cap",
        description="""
Default is market_cap. Options include: volume_1d, volume_7d, volume_30d,
volume_total, volume_change_1d,
volume_change_7d, volume_change_30d, sales_1d, sales_7d, sales_30d,
sales_total, sales_change_1d,
sales_change_7d, sales_change_30d,
floor_price, market_cap. Required only for 'action=rank'
    """,
    )


class NFTExpert(BaseTool):
    name = "NFT"
    description = "A tool for searching NFT collections or getting collection rankings."
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        action: str,
        keyword: Optional[str] = None,
        sort_field: Optional[str] = "market_cap",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        if action == "search":
            if keyword is None:
                return "Error: A keyword is required for search operation."
            return self.search_nft_collections(keyword)
        elif action == "rank":
            return self.collection_ranking(sort_field)
        else:
            return (
                "Error: Unknown operation type. "
                "Please specify 'action' as 'search' or 'rank'."
            )

    async def _arun(
        self,
        action: str,
        keyword: Optional[str] = None,
        sort_field: Optional[str] = "market_cap",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return self._run(action, keyword, sort_field, run_manager)

    @staticmethod
    def search_nft_collections(keyword: str) -> str:
        """Search for NFT collections."""
        url = "https://restapi.nftscan.com/api/v2/collections/filters"
        payload = json.dumps(
            {
                "contract_address_list": [],
                "name_fuzzy_search": "false",
                "show_collection": "false",
                "sort_direction": "desc",
                "sort_field": "floor_price",
                "name": "",
                "symbol": keyword,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": f"{settings.NFTSCAN_API_KEY}",
        }

        response = requests.post(url, headers=headers, data=payload)
        return response.text

    @staticmethod
    def collection_ranking(sort_field: str) -> str:
        """Search for NFT collections ranking."""
        url = f"https://restapi.nftscan.com/api/v2/statistics/ranking/collection?sort_field={sort_field}&sort_direction=desc&limit=20"

        headers = {"X-API-KEY": f"{settings.NFTSCAN_API_KEY}"}
        response = requests.get(url, headers=headers)
        return response.text


if __name__ == "__main__":
    nft_expert = NFTExpert()
    print(nft_expert.search_nft_collections("BAYC"))
    print(nft_expert.collection_ranking("market_cap"))
