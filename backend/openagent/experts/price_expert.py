from typing import Optional, Type

import ccxt
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class ARGS(BaseModel):
    coin: str = Field(description="coin symbol")


class PriceExpert(BaseTool):
    name = "price"
    description = "use this tool to get the price of a coin."
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        coin: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        coin: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return f"The price of {coin} is {fetch_price(coin)}"


_binance = ccxt.binance()


def fetch_price(base: str, quote: str = "USDT") -> float:
    ticker = _binance.fetch_trades(f"{base}/{quote}", limit=1)
    last = ticker[0]["price"]
    return last
