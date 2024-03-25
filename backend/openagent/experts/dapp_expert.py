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
        description="""query type, default is 'all'. \
option: "social", "governance", "donation", "collectible", "exchange", \
"defi_tvl", "defi_lst", "defi_dex_total", "defi_stable_coin", "defi_derivative"."""
    )


class DappExpert(BaseTool):
    name = "dapp"
    description = """Use this tool to query dapp or defi projects information. \
"""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        query_type: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        query_type: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_dapp(query_type)


async def fetch_dapp(query_type: str):
    host = settings.RSS3_AI_API
    dapp_prefix = "dapps"
    defi_prefix = "defi"
    is_defi = query_type in {
        "defi_tvl",
        "defi_lst",
        "defi_dex_total",
        "defi_stable_coin",
        "defi_derivative",
    }

    prefix = defi_prefix if is_defi else dapp_prefix

    url = f"""{host}/m1/v2/{prefix}?action={query_type}&network=ethereum&limit=10"""
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
        async with session.get(url, headers=headers) as resp:
            result = await resp.text()
            result += "\nAdd a one-sentence short introduction to each item, \
but do not display the URL.\n"
            return result
