import json
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from moralis import evm_api
from pydantic import BaseModel, Field

from openagent.conf.env import settings


class NFTRankingArgs(BaseModel):
    limit: int = Field(description="Number of collections to return", default=10)


class NFTRankingExecutor(BaseTool):
    name = "NFTRankingExecutor"
    description = "A tool for getting NFT collection rankings."
    args_schema: Type[NFTRankingArgs] = NFTRankingArgs

    def _run(
        self,
        limit: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.collection_ranking(limit)

    async def _arun(
        self,
        limit: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return self._run(limit, run_manager)

    @staticmethod
    def collection_ranking(limit: int) -> str:
        if settings.MORALIS_API_KEY is None:
            return "Please set MORALIS_API_KEY in the environment"
        by_market_cap = evm_api.market_data.get_top_nft_collections_by_market_cap(
            api_key=settings.MORALIS_API_KEY,
        )
        limit = min(limit, len(by_market_cap))
        result = by_market_cap[0:limit]
        return json.dumps(
            list(
                map(
                    lambda x: {
                        "collection_title": x["collection_title"],
                        "collection_image": x["collection_image"],
                        "floor_price_usd": x["floor_price_usd"],
                        "collection_address": x["collection_address"],
                    },
                    result,
                )
            )
        )


if __name__ == "__main__":
    ranking = NFTRankingExecutor.collection_ranking(4)
    print(ranking)
