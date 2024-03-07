from typing import Optional, Type

import aiohttp

from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

from openagent.dto.mutation import Swap
from openagent.tool import (
    get_token_data_by_key,
    select_best_token,
)


class ParamSchema(BaseModel):
    from_token: str = Field(
        description="""extract the from-side cryptocurrencies mentioned in the query,
like: "BTC", "ETH", "RSS3", "USDT", "USDC" and etc. Default is "ETH"."""
    )

    to_token: str = Field(
        description="""extract the to-side cryptocurrencies mentioned in the query,
like: "BTC", "ETH", "RSS3", "USDT", "USDC" and etc. Default is "ETH"."""
    )

    amount: str = Field(
        description="""extract the amount of cryptocurrencies mentioned in the query,
like: "0.1", "1", "10" and etc. Default is "1"."""
    )


class SwapTool(BaseTool):
    name = "swap"
    description = """Use this tool to extract structured information from the user's query,
whenever the query is about swap or buy some cryptocurrencies.\n
"""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        from_token: str,
        to_token: str,
        amount: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        from_token: str,
        to_token: str,
        amount: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_swap(from_token, to_token, amount)


async def fetch_swap(from_token: str, to_token: str, amount: str):
    url = """https://li.quest/v1/tokens"""
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            logger.info(f"fetching {url}")
            token_list = await resp.json()
            token_list["tokens"]["1"]
            res = {"from": from_token, "to": to_token, "amount": amount}
            results = [
                select_best_token(res["from"]),
                select_best_token(res["to"]),
            ]
            swap = Swap(
                from_token=get_token_data_by_key(results[0], "symbol"),
                from_token_address=get_token_data_by_key(results[0], "address"),
                to_token=get_token_data_by_key(results[1], "symbol"),
                to_token_address=get_token_data_by_key(results[1], "address"),
                amount=res.get("amount", "1"),
            )
            return swap
