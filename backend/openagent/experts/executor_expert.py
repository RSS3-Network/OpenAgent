from typing import Any, Optional

import aiohttp
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger

from openagent.agent.ctx_var import chat_req_ctx
from openagent.conf.env import settings


class ExecutorExpert(BaseTool):
    name = "wallet"
    description = """Use this tool to query wallet information. for example: \
"what is my wallet balance", "what is my wallet address" and etc. \
"""

    def _run(
        self,
        *args: Any,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        *args: Any,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_executor()


async def fetch_executor():
    host = settings.EXECUTOR_API
    req_ctx = chat_req_ctx.get()
    user_id = req_ctx.user_id
    url = f"""{host}/executors/{user_id}"""
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
        async with session.get(url, headers=headers) as resp:
            return await resp.text()
