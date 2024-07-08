import json
from typing import Dict, Optional

import chainlit as cl
import chainlit.data as cl_data
from chainlit.cli import run_chainlit
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import FunctionMessage
from loguru import logger

from openagent.agent.function_agent import get_agent
from openagent.conf.env import settings

# Set up the data layer
cl_data._data_layer = SQLAlchemyDataLayer(conninfo=settings.VEC_DB_CONNECTION)


def setup_runnable():
    """Set up the runnable agent."""
    agent = get_agent("")
    cl.user_session.set("runnable", agent)


def initialize_memory() -> ConversationBufferMemory:
    """Initialize conversation memory."""
    return ConversationBufferMemory(return_messages=True)


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


async def handle_function_message(message: FunctionMessage, msg: cl.Message):
    """Handle FunctionMessage type of messages."""
    if message.name == "swap":
        swap_dict = json.loads(message.content)
        from_chain = swap_dict["chain_id"]
        to_chain = swap_dict["chain_id"]
        from_token_ = swap_dict["from_token_address"]
        to_token = swap_dict["to_token_address"]
        from_amount = swap_dict["amount"]

        widget = (
            f"""<iframe src="{settings.WIDGET_URL}/swap?fromAmount={from_amount}&"""
            f"""fromChain={from_chain}&fromToken={from_token_}&toChain={to_chain}&"""
            f"""toToken={to_token}" width="400" height="700"></iframe>"""
        )
        await msg.stream_token(widget)


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
    except Exception as e:
        logger.error(f"Error processing message: {e}")

    await msg.send()
    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(msg.content)


def start_ui():
    run_chainlit(__file__)


if __name__ == "__main__":
    start_ui()
