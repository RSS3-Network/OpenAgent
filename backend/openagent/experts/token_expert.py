from typing import Optional, Type

import aiohttp
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

from openagent.conf.env import settings


class ParamSchema(BaseModel):
    query_type: str = Field(
        description="""query type, option: "market_cap", "token_price", \
"token_volume", "token_supply", "popular_tokens"."""
    )
    token_name: str = Field(
        description="""token name. default is "eth". option: "wbtc", "eth", \
"usdt", "usdc", "bnb" and etc.""",
        default="",
    )


class TokenExpert(BaseTool):
    name = "token"
    description = """Use this tool to query cryptocurrency information.\n\
"""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        query_type: str,
        token_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        query_type: str = "",
        token_name: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_token(query_type, token_name)


async def fetch_token(query_type: str, token_name: str):
    host = settings.RSS3_AI_API
    if query_type == "popular_tokens":
        url = f"""{host}/m1/v2/tokens?limit=10&network=ethereum"""
    else:
        url = f"""{host}/m1/v2/tokens?action={query_type}&address={token_name}&network=ethereum"""
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
        async with session.get(url, headers=headers) as resp:
            result = await resp.text()
            result += "\nThe monetary unit is USD.\n"
            return result
