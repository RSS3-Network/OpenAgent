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
        description="""query type, option: block_height,\
gas_price."""
    )
    network: str = Field(
        description="blockchain network, option: arbitrum,\
binance_smart_chain, ethereum, polygon"
    )


class NetworkExpert(BaseTool):
    name = "network"
    description = """use this tool to query a blockchain network overview \
data about block_height, gas_price.\n\
"""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        query_type: str,
        network: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        query_type: str,
        network: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_network(query_type, network)


async def fetch_network(query_type: str, network: str):
    host = settings.RSS3_AI_API
    url = f"""{host}/m1/v2/networks?action={query_type}&network={network}&limit=10"""
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
        async with session.get(url, headers=headers) as resp:
            return await resp.text()
