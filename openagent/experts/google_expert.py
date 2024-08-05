from typing import Optional, Type

from langchain import SerpAPIWrapper
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class GoogleSchema(BaseModel):
    query: str = Field(description="The search query keywords for Google search.")


async def google_search(query: str) -> str:
    search_wrapper = SerpAPIWrapper(
        search_engine="google",
        params={"engine": "google"},
    )
    return search_wrapper.run(query)


class GoogleExpert(BaseTool):
    name = "GoogleExecutor"
    description = """A versatile search tool that retrieves up-to-date information from the web. \
Use for current events, project details, fact-checking, and general research across various topics."""
    args_schema: Type[GoogleSchema] = GoogleSchema

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
        return await google_search(query)
