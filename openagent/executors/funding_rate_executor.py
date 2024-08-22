import json
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
    exchange: str = Field(description="Name of the exchange (ccxt supported), e.g., 'binance'")
    symbol: str = Field(description="Trading pair symbol, e.g., 'BTC/USDT'")


class FundingRateExecutor(BaseTool):
    name = "FundingRateExecutor"
    description = "Use this tool to get the funding rate of a trading pair."
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        exchange: str,
        symbol: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            return json.dumps(fetch_funding_rate(exchange, symbol))
        except Exception as e:
            return f"error: {e}"

    async def _arun(
        self,
        exchange: str,
        symbol: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        try:
            return json.dumps(fetch_funding_rate(exchange, symbol))
        except Exception as e:
            return f"error: {e}"


def fetch_funding_rate(exchange_name: str, symbol: str) -> float:
    try:
        if not symbol.endswith(":USDT"):
            symbol = f"{symbol}:USDT"
        exchange_class = getattr(ccxt, exchange_name)
        exchange = exchange_class()

        funding_rate = exchange.fetch_funding_rate(symbol)
        return funding_rate
    except Exception as e:
        logger.warning(f"Fetch funding rate error from {exchange_name}: {e}")
        raise e


if __name__ == "__main__":
    tool = FundingRateExecutor()
    print(tool.run(tool_input={"exchange": "binance", "symbol": "BTC/USDT:USDT"}))
