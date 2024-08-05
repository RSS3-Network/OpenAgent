from typing import Optional, Type

import ccxt
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field


class ARGS(BaseModel):
    token: str = Field(description="token symbol")


class PriceExpert(BaseTool):
    name = "PriceExecutor"
    description = "use this tool to get the price of a token."
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        token: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        token: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return f"The price of {token} is {fetch_price(token)}"


_exchanges = [ccxt.binance(), ccxt.okx(), ccxt.gateio(), ccxt.mexc()]


def fetch_price(base: str, quote: str = "USDT") -> float:
    for exchange in _exchanges:
        try:
            trades = exchange.fetch_trades(f"{base.upper()}/{quote}", limit=1)
            last = trades[0]["price"]
            return last
        except Exception as e:  # noqa
            logger.warning(f"fetch price error from {exchange.id}: {e}")
    raise Exception(f"no market found for {base}")
