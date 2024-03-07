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
    query_type: str = Field(description="""query type, fixed to "popular".""")


class AccountTool(BaseTool):
    name = "account"
    description = """Use this tool to query active users/accounts information. \
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
        return await fetch_account(query_type)


async def fetch_account(query_type: str):
    host = settings.RSS3_AI_API

    url = f"""{host}/m1/v2/accounts?action={query_type}&network=ethereum&limit=10"""
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
        async with session.get(url, headers=headers) as resp:
            return await resp.text()
