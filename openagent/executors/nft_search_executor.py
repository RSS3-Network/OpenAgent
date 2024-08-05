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


class NFTSearchArgs(BaseModel):
    keyword: str = Field(description="NFT symbol or collection name for search")


class NFTSearchExecutor(BaseTool):
    name = "NFTSearchTool"
    description = "A tool for searching NFT collections."
    args_schema: Type[NFTSearchArgs] = NFTSearchArgs

    def _run(
        self,
        keyword: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.search_nft_collections(keyword)

    async def _arun(
        self,
        keyword: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return self._run(keyword, run_manager)

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
