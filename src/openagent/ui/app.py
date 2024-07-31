import json
from typing import Dict, Optional

import chainlit as cl
import chainlit.data as cl_data
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import FunctionMessage
from langchain_core.utils.json import parse_json_markdown
from loguru import logger

from openagent.agent.function_agent import get_agent
from openagent.conf.env import settings


def enable_auth():
    auth_settings = [settings.CHAINLIT_AUTH_SECRET, settings.OAUTH_AUTH0_CLIENT_ID, settings.OAUTH_AUTH0_CLIENT_SECRET, settings.OAUTH_AUTH0_DOMAIN]
    return all(arg is not None for arg in auth_settings)


if enable_auth():
    # Set up the data layer
    cl_data._data_layer = SQLAlchemyDataLayer(conninfo=settings.DB_CONNECTION)


def setup_runnable():
    """Set up the runnable agent."""
    agent = get_agent("")
    cl.user_session.set("runnable", agent)


def initialize_memory() -> ConversationBufferMemory:
    """Initialize conversation memory."""
    return ConversationBufferMemory(return_messages=True)


if enable_auth():

    @cl.oauth_callback
    def oauth_callback(
        provider_id: str,
        token: str,
        raw_user_data: Dict[str, str],
        default_user: cl.User,
    ) -> Optional[cl.User]:
        """OAuth callback function."""
        return default_user


@cl.on_chat_start
async def on_chat_start():
    """Callback function when chat starts."""
    cl.user_session.set("memory", initialize_memory())
    setup_runnable()


if enable_auth():

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
        setup_runnable()


def build_token(token_symbol: str, token_address: str):
    return f"{token_symbol}{'--' + token_address.lower() if token_symbol != 'ETH' else ''}"


async def handle_function_message(message: FunctionMessage, msg: cl.Message):
    """Handle FunctionMessage type of messages."""
    if message.name == "SwapExecutor":
        swap_dict = json.loads(message.content)
        await do_stream_swap_widget(msg, swap_dict)
    elif message.name == "TransferExecutor":
        transfer_dict = json.loads(message.content)
        await do_stream_transfer_widget(msg, transfer_dict)

async def do_stream_swap_widget(msg, swap_dict):
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
        f"""toToken={build_token(to_token, to_token_address)}&fromAmount={from_amount}" width="400" height="700"></iframe>"""
    )
    await msg.stream_token(widget)


async def do_stream_transfer_widget(msg, transfer_dict):
    token = transfer_dict["token"]
    to_address = transfer_dict["to_address"]
    amount = transfer_dict["amount"]
    chain_name = transfer_dict.get("chain_name", "ethereum")

    url = (
        f"http://localhost:3000/?token={token}"
        f"&amount={amount}&toAddress={to_address}&chainName={chain_name}"
    )

    iframe_html = f"""
        <iframe src="{url}" width="100%" height="600px" style="border:none;">
        </iframe>
        """
    await msg.stream_token(iframe_html)




@cl.on_message
async def on_message(message: cl.Message):
    """Callback function to handle user messages."""
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory
    runnable = cl.user_session.get("runnable")

    msg = cl.Message(content="")

    try:
        async for chunk in runnable.astream(
            {"input": message.content}, config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)])
        ):
            if "output" in chunk:
                await msg.stream_token(chunk["output"])
            elif "messages" in chunk:
                for message in chunk["messages"]:
                    if isinstance(message, FunctionMessage):
                        await handle_function_message(message, msg)
                    else:
                        await react_tool_call_handle(message, msg)
    except Exception as e:
        logger.exception(e)

    await msg.send()
    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(msg.content)


async def react_tool_call_handle(message, msg):
    try:
        action_dict = parse_json_markdown(message.content)
        if "type" in action_dict:
            if action_dict["type"] == "SwapExecutor":
                await do_stream_swap_widget(msg, action_dict)
            elif action_dict["type"] == "TransferExecutor":
                await do_stream_transfer_widget(msg, action_dict)
    except Exception as e:
        logger.warning("Failed to handle react tool call message", e)
