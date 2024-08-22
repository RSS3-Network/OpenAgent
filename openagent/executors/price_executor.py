import asyncio
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
    token: str = Field(description="token symbol, e.g., 'ETH', 'BTC'")


class PriceExecutor(BaseTool):
    name = "PriceExecutor"
    description = "use this tool to get the price widget of a token."
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        token: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return asyncio.run(fetch_price(token))

    async def _arun(
        self,
        token: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return await fetch_price(token)


async def fetch_price(token: str) -> str:
    url = f"https://pro-api.coingecko.com/api/v3/search?query={token}"

    key = settings.COINGECKO_API_KEY
    headers = {"accept": "application/json", "x-cg-pro-api-key": key}

    response = requests.get(url, headers=headers)
    token_: dict = json.loads(response.text)["coins"][0]
    token_id_ = token_["id"]

    url = (
        f"https://pro-api.coingecko.com/api/v3/simple/price?ids={token_id_}&"
        f"vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&"
        f"include_24hr_change=true&include_last_updated_at=true"
    )

    headers = {"accept": "application/json", "x-cg-pro-api-key": key}

    response = requests.get(url, headers=headers)

    return response.text


if __name__ == "__main__":
    print(asyncio.run(fetch_price("eth")))
