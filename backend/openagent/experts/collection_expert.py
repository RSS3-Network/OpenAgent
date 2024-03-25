import json
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
        description="""
    query type. default is 'market_cap'. option: "average_price", "floor_price", "market_cap", \
    "sales_7d", "sales_change_7d", "volume_7d", "volume_change_7d", \
    "sales_total", "volume_total", "popular_nfts".
    """,
    )
    nft_name: str = Field(
        description="""nft collection name. default is ''. option: "azuki", \
"cryptopunks", "bayc", "doodles" or other nft name etc.""",
        default="",
    )


class CollectionExpert(BaseTool):
    name = "collection"
    description = """Use this tool to get some information about the NFT collection"""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        query_type: str = "",
        nft_name: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        query_type: str = "",
        nft_name: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_collections(query_type, nft_name)


async def fetch_collections(query_type: str, nft_name: str):
    host = settings.RSS3_AI_API_BASE
    if query_type == "popular_nfts":
        url = f"""{host}/m1/v2/collections?limit=10&network=ethereum&order=popular"""
    else:
        action_str = f"action={query_type}" if query_type else ""
        address_str = f"&address={nft_name}" if nft_name else ""
        url = f"""{host}/m1/v2/collections?network=ethereum&{action_str}{address_str}"""
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
        async with session.get(url, headers=headers) as resp:
            info = await resp.text()
            data = json.loads(info)
            for item in data.get("data", {}).get("items", []):
                item["nft_collection_website"] = (
                    "https://etherscan.io/token/" + item.get("nft_collection_addr", "")
                )
                keys_to_remove = [k for k, v in item.items() if v == 0 or v == ""]
                for key in keys_to_remove:
                    item.pop(key, None)

            data = str(data).replace("'", '"')
            data += "\nWhen an official website URL is available in the tool's results, \
it will be included in the response.\n"
            return data
