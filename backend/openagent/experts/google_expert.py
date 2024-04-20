from typing import Optional, Type

from langchain import SerpAPIWrapper
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class SearchSchema(BaseModel):
    query: str = Field(description="should be a search query")
    gl: str = Field(
        description="should be a country code, such as 'us' or 'cn' or 'jp' and so on"
    )
    hl: str = Field(
        description="should be a language code, such as 'en' or 'zh-cn' or \
'ja' and so on"
    )


class GoogleExpert(BaseTool):
    name = "google-search"
    description = "useful for when you need to answer questions\
about current events, this tool's priority is lower than other tool."
    args_schema: Type[SearchSchema] = SearchSchema

    def _run(
        self,
        query: str,
        gl: str = "us",
        hl: str = "en",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        query: str,
        gl: str = "us",
        hl: str = "en",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        engine: str = "google"
        """Use the tool asynchronously."""
        # search_run = DuckDuckGoSearchRun()
        search_wrapper = SerpAPIWrapper(
            search_engine=engine,
            params={"engine": engine, "gl": gl, "hl": hl},
        )
        return search_wrapper.run(query)
