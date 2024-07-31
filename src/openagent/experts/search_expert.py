from typing import Optional, Type

from langchain import SerpAPIWrapper
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class SearchSchema(BaseModel):
    query: str = Field(description="The search query keywords.")


async def google_search(query: str) -> str:
    search_wrapper = SerpAPIWrapper(
        search_engine="google",
        params={"engine": "google"},
    )
    return search_wrapper.run(query)


class SearchExpert(BaseTool):
    name = "SearchExecutor"
    description = """
    A versatile search tool that can perform various types of searches based on the query type:
    - For queries about project introductions, current events or real-time information, use Google search."""
    args_schema: Type[SearchSchema] = SearchSchema

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
