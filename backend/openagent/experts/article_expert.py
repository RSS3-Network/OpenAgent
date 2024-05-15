import json
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.index.pgvector_store import store


class ARGS(BaseModel):
    keyword: str = Field(
        description="keyword to search for",
    )


class ArticleExpert(BaseTool):
    name = "article"
    description = (
        "A tool for searching web3-related articles. If you lack knowledge about web3, "
        "you can use this tool to find relevant articles that can help answer "
        "your questions. Provide a keyword or phrase related to the topic "
        "you want to search for, and the tool will return a list of "
        "relevant article excerpts. "
        "The articles are sourced from IQWiki and Mirror."
    )
    args_schema: Type[ARGS] = ARGS

    def _run(
        self,
        keyword: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.search_articles(keyword)

    async def _arun(
        self,
        keyword: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return self.search_articles(keyword)

    @staticmethod
    def search_articles(keyword: str) -> str:
        retriever = store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.8, "k": 3},
        )
        res = retriever.get_relevant_documents(keyword)
        docs = list(map(lambda x: x.page_content, res))
        return json.dumps(docs)


if __name__ == "__main__":
    expert = ArticleExpert()
    print(expert._run("vitalik's father"))
