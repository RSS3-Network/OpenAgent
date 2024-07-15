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
    chain: str = Field(
        description="chain name,options:btc-mainnet,eth-mainnet,optimism-mainnet,arbitrum-mainnet,bsc-mainnet"
    )
    wallet_address: str = Field(description="wallet address")


class TokenBalanceTool(BaseTool):
    name = "token-balance"
    description = "get the token balance of a wallet."
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
    c = CovalentClient(settings.COVALENT_API_KEY)
    b = c.balance_service.get_token_balances_for_wallet_address(chain, address)
    if b.error:
        return b.error_message
    return json.dumps(
        list(
            map(
                lambda x: {
                    "contract_ticker_symbol": x.contract_ticker_symbol,
                    "balance": x.balance,
                    "pretty_quote": x.pretty_quote,
                },
                b.data.items,
            )
        )
    )


if __name__ == "__main__":
    print(fetch_balance("eth-mainnet", "0x33c0814654fa367ce67d8531026eb4481290e63c"))
