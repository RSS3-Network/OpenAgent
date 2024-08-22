import json
from typing import Dict, Optional

import chainlit as cl
import chainlit.data as cl_data
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from loguru import logger

from openagent.conf.env import settings
from openagent.conf.llm_provider import get_available_providers
from openagent.ui.profile import profile_name_to_provider_key, provider_to_profile
from openagent.workflows.member import members
from openagent.workflows.workflow import build_workflow


def enable_auth():
    auth_settings = [
        settings.CHAINLIT_AUTH_SECRET,
        settings.OAUTH_AUTH0_CLIENT_ID,
        settings.OAUTH_AUTH0_CLIENT_SECRET,
        settings.OAUTH_AUTH0_DOMAIN,
    ]
    return all(arg for arg in auth_settings)


if enable_auth():
    # Set up the data layer
    cl_data._data_layer = SQLAlchemyDataLayer(conninfo=settings.DB_CONNECTION)

    @cl.oauth_callback
    def oauth_callback(
        provider_id: str,
        token: str,
        raw_user_data: Dict[str, str],
        default_user: cl.User,
    ) -> Optional[cl.User]:
        """OAuth callback function."""
        return default_user

    @cl.on_chat_resume
    async def on_chat_resume(thread: cl_data.ThreadDict):
        """Callback function when chat resumes."""
        memory = initialize_memory()
        root_messages = [m for m in thread["steps"]]
        for message in root_messages:
            if message["type"] == "user_message":
                memory.chat_memory.add_user_message(message["output"])
            else:
                memory.chat_memory.add_ai_message(message["output"])

        cl.user_session.set("memory", memory)
        profile = cl.user_session.get("chat_profile")
        provider_key = profile_name_to_provider_key(profile)
        llm = get_available_providers()[provider_key]
        setup_runnable(llm)


def setup_runnable(llm: BaseChatModel):
    """Set up the runnable agent."""
    agent = build_workflow(llm)
    cl.user_session.set("runnable", agent)


def initialize_memory() -> ConversationBufferMemory:
    """Initialize conversation memory."""
    return ConversationBufferMemory(return_messages=True)


@cl.set_chat_profiles
async def chat_profile():
    providers = get_available_providers()
    profiles = list(map(provider_to_profile, providers.keys()))
    profiles = [profile for profile in profiles if profile is not None]

    return profiles


@cl.on_chat_start
async def on_chat_start():
    """Callback function when chat starts."""
    cl.user_session.set("memory", initialize_memory())
    profile = cl.user_session.get("chat_profile")
    provider_key = profile_name_to_provider_key(profile)
    llm = get_available_providers()[provider_key]
    setup_runnable(llm)


def build_token(token_symbol: str, token_address: str):
    return f"{token_symbol}{'--' + token_address.lower() if token_symbol != 'ETH' else ''}"


@cl.on_message
async def on_message(message: cl.Message):
    """Callback function to handle user messages."""
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory

    profile = cl.user_session.get("chat_profile")
    provider_key = profile_name_to_provider_key(profile)
    llm = get_available_providers()[provider_key]

    setup_runnable(llm)
    runnable = cl.user_session.get("runnable")

    msg = cl.Message(content="")
    agent_names = [member["name"] for member in members]

    async for event in runnable.astream_events(
        {"messages": [*memory.chat_memory.messages, HumanMessage(content=message.content)]},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)]),
        version="v1",
    ):
        kind = event["event"]
        if kind == "on_tool_end":
            await handle_tool_end(event, msg)
        elif kind == "on_chat_model_stream":  # noqa
            if event["metadata"]["langgraph_node"] in agent_names:
                content = event["data"]["chunk"].content
                if content:
                    await msg.stream_token(content)

    await msg.send()
    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(msg.content)


async def handle_tool_end(event, msg):
    if event["name"] == "SwapExecutor":
        output = event["data"]["output"]
        swap_dict = json.loads(output)
        logger.info(swap_dict)
        from_chain = swap_dict["from_chain_name"]
        to_chain = swap_dict["to_chain_name"]
        from_token_ = swap_dict["from_token"]
        from_token_address = swap_dict["from_token_address"]
        to_token = swap_dict["to_token"]
        to_token_address = swap_dict["to_token_address"]
        from_amount = swap_dict["amount"]

        widget = (
            f"""<iframe style="swap" src="https://widget.rango.exchange/?fromBlockchain={from_chain}&"""
            f"""fromToken={build_token(from_token_, from_token_address)}&toBlockchain={to_chain}&"""
            f"""toToken={build_token(to_token, to_token_address)}&fromAmount={from_amount}"
             width="400" height="700"></iframe>"""
        )
        await msg.stream_token(widget)

    if event["name"] == "TransferExecutor":
        output = event["data"]["output"]
        transfer_dict = json.loads(output)
        token = transfer_dict["token"]
        token_address = transfer_dict["token_address"]
        to_address = transfer_dict["to_address"]
        amount = transfer_dict["amount"]

        url = f"/widget/transfer?token={token}&tokenAddress={token_address}&amount={amount}&toAddress={to_address}"

        iframe_html = f"""
                <iframe src="{url}" width="100%" height="600px" style="border:none;">
                </iframe>
                """
        await msg.stream_token(iframe_html)

    if event["name"] == "PriceExecutor":
        output = event["data"]["output"]
        price_dict = json.loads(output)
        widget = f"""<iframe src="/widget/price-chart?token={list(price_dict.keys())[0]}" height="400px"></iframe>"""  # noqa
        await msg.stream_token(widget)
