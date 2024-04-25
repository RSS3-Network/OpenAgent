import json
from typing import Optional, Type

import requests
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class ARGS(BaseModel):
    keyword: str = Field(description="keyword")


class DuneExpert(BaseTool):
    name = "dune-dashboard-retriever"
    description = (
        "use this tool to search the dune dashboard."
        " it will return the embedded iframe of the dashboard."
    )
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        coin: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        coin: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return json.dumps(fetch_dashboards(coin))


def fetch_dashboards(kw: str) -> dict:
    url = f"https://devnet.rss3.io/search/dune/search?keyword={kw}"
    payload = {}  # type: ignore
    headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


if __name__ == "__main__":
    print(fetch_dashboards("bitcoin price"))
