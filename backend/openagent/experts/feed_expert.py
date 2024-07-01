from typing import Optional, Type

import aiohttp
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

from openagent.agent.system_prompt import FEED_PROMPT
from openagent.conf.env import settings


class ParamSchema(BaseModel):
    address: str = Field(
        description="""wallet address or blockchain domain name,\
hint: vitalik's address is vitalik.eth"""
    )


class FeedExpert(BaseTool):
    name = "feed"
    description = """Use this tool to get the activities of a wallet address or \
blockchain domain name and know what this address has done or doing recently."""
    args_schema: Type[ParamSchema] = ParamSchema

    def _run(
        self,
        address: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        address: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_feeds(address)


async def fetch_feeds(address: str):
    host = settings.RSS3_DATA_API + "/accounts"
    url = f"""{host}/{address}/activities?limit=10&action_limit=5&direction=out"""
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        logger.info(f"fetching {url}")
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()

    formatted_activities = []
    for activity in data["data"]:
        formatted_activity = f"## Transaction on {activity['network']}\n"
        formatted_activity += f"- **Type**: {activity['type']}\n"
        formatted_activity += f"- **Status**: {activity['status']}\n"
        formatted_activity += f"- **Timestamp**: {activity['timestamp']}\n"

        if "actions" in activity:
            formatted_activity += "### Actions:\n"
            for action in activity["actions"]:
                formatted_activity += (
                    f"- {action['type']} from {action['from']} to {action['to']}\n"
                )
                if "metadata" in action:
                    for key, value in action["metadata"].items():
                        formatted_activity += f"  - {key}: {value}\n"

        formatted_activities.append(formatted_activity)

    activities_data = "\n\n".join(formatted_activities)

    result = FEED_PROMPT.format(address=address, activities_data=activities_data)

    return result
