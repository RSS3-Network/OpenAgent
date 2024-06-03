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
    chain: str = Field(description="block chain, options:ethereum, bitcoin")


class BlockStatExpert(BaseTool):
    name = "block_chain_stat"
    description = (
        "use this tool to get block chain stat, like block height, gas fee, etc."
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
        try:
            return fetch_stat(chain)
        except Exception as e:
            return f"error: {e}"


_exchanges = [ccxt.binance(), ccxt.okx(), ccxt.gateio(), ccxt.mexc()]


def fetch_stat(chain) -> str:
    url = f"https://api.blockchair.com/{chain}/stats"

    payload = {}  # type: ignore
    headers = {"accept": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text


if __name__ == "__main__":
    print(fetch_stat("bitcoin"))
