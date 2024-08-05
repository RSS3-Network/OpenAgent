from typing import Optional, Type

import ccxt
import requests
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class ARGS(BaseModel):
    chain: str = Field(
        description="The blockchain to fetch statistics for. "
        "Options: ethereum, bitcoin, bitcoin-cash, litecoin,"
        " bitcoin-sv, dogecoin, dash, groestlcoin,"
        " zcash, ecash, bitcoin/testnet"
    )


class BlockStatExecutor(BaseTool):
    name = "BlockChainStatExecutor"
    description = (
        "get blockchain statistics such as block height, "
        "transaction count, gas fees, and more. "
        "Supported blockchains include ethereum, Bitcoin, Bitcoin Cash, "
        "Litecoin, Bitcoin SV, Dogecoin, Dash, Groestlcoin, Zcash, eCash, "
        "and Bitcoin Testnet."
    )
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        chain: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return fetch_stat(chain)

    async def _arun(
        self,
        chain: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return fetch_stat(chain)


_exchanges = [ccxt.binance(), ccxt.okx(), ccxt.gateio(), ccxt.mexc()]


def fetch_stat(chain) -> str:
    url = f"https://api.blockchair.com/{chain}/stats"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching data: {response.status_code}, {response.text}"


if __name__ == "__main__":
    print(fetch_stat("ethereum"))
