import json
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.conf.env import settings


class ARGS(BaseModel):
    chain: str = Field(description="chain name,options:eth,optimism,arbitrum,bsc")

    wallet_address: str = Field(description="wallet address")


class NFTBalanceExecutor(BaseTool):
    name = "NFTBalanceExecutor"
    description = "get the nft asset of a wallet."
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        chain: str,
        wallet_address: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return fetch_balance(chain, wallet_address)

    async def _arun(
        self,
        chain: str,
        wallet_address: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return fetch_balance(chain, wallet_address)


def fetch_balance(chain: str, address: str) -> str:
    if settings.MORALIS_API_KEY is None:
        return "Please set MORALIS_API_KEY in the environment"
    from moralis import evm_api

    params = {"chain": chain, "format": "decimal", "media_items": False, "address": address}

    result = evm_api.nft.get_wallet_nfts(
        api_key=settings.MORALIS_API_KEY,
        params=params,
    )

    return json.dumps(
        list(
            map(
                lambda x: {
                    "amount": x["amount"],
                    "name": x["name"],
                    "symbol": x["symbol"],
                },
                result["result"],
            )
        )
    )


if __name__ == "__main__":
    print(fetch_balance("eth", "0x33c0814654fa367ce67d8531026eb4481290e63c"))
