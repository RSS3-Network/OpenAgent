from typing import Optional, Type

import requests
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.conf.env import settings


class DuneSchema(BaseModel):
    query: str = Field(description="The search query keywords for Dune dashboard search.")


async def dune_search(query: str) -> str:
    url = f"{settings.RSS3_SEARCH_API}/dune/search?keyword={query}"
    headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("GET", url, headers=headers)
    return response.text


class DuneExpert(BaseTool):
    name = "DuneExecutor"
    description = """This tool searches for charts, data visualizations, and dashboards on Dune Analytics. \
Use this tool to find visual representations of blockchain data, trend analysis, and market overviews."""
    args_schema: Type[DuneSchema] = DuneSchema

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return await dune_search(query)
