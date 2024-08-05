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


class ARGS(BaseModel):
    order: str = Field(
        description="sort result by field, default: market_cap_desc. options: market_cap_desc," "market_cap_asc,volume_desc,volume_asc"
    )
    size: int = Field(description="number of coins to return, default: 20")


class CoinMarketExecutor(BaseTool):
    name = "CoinMarketExecutor"

    description = "query coins sorted by market cap, volume."
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        order: str,
        size: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        if settings.COINGECKO_API_KEY is None:
            return "Please set COINGECKO_API_KEY in the environment"
        return json.dumps(fetch_coins_with_market(order, size))

    async def _arun(
        self,
        order: str,
        size: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        if settings.COINGECKO_API_KEY is None:
            return "Please set COINGECKO_API_KEY in the environment"
        return json.dumps(fetch_coins_with_market(order, size))


def fetch_coins_with_market(order: str, size: int = 20) -> list:
    url = f"https://pro-api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order={order}&per_page={size}"

    headers = {
        "accept": "application/json",
        "x-cg-pro-api-key": settings.COINGECKO_API_KEY,
    }

    response = requests.get(url, headers=headers)

    res = json.loads(response.text)
    return list(
        map(
            lambda x: {
                "symbol": x["symbol"],
                "name": x["name"],
                "current_price": x["current_price"],
                "fully_diluted_valuation": x["fully_diluted_valuation"],
                "total_volume": x["total_volume"],
            },
            res,
        )
    )


if __name__ == "__main__":
    print(fetch_coins_with_market("market_cap_desc"))
