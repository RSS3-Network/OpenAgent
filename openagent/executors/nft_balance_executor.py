import json
from typing import Optional, Type

from covalent import CovalentClient
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.conf.env import settings


class ARGS(BaseModel):
    chain: str = Field(description="chain name,options:eth-mainnet,optimism-mainnet,arbitrum-mainnet,bsc-mainnet")
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
    if settings.COVALENT_API_KEY is None:
        return "Please set COVALENT_API_KEY in the environment"
    print(settings.COVALENT_API_KEY)
    c = CovalentClient('ckey_docs')
    b = c.nft_service.get_nfts_for_address(chain, address)
    if b.error:
        return b.error_message
    return json.dumps(
        list(
            map(
                lambda x: {
                    "contract_name": x.contract_name,
                    "contract_ticker_symbol": x.contract_ticker_symbol,
                    "balance": x.balance,
                    "pretty_floor_price_quote": x.pretty_floor_price_quote,
                },
                b.data.items,
            )
        )
    )


if __name__ == "__main__":
    print(fetch_balance("eth-mainnet", "0x33c0814654fa367ce67d8531026eb4481290e63c"))
