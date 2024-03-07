import uuid
from random import random

import chainlit as cl
from chainlit import Message
from langchain.callbacks import LLMonitorCallbackHandler
from loguru import logger

from openagent.agent.ctx_var import resp_msg_id, chat_req_ctx
from openagent.agent.function_agent import get_agent
from openagent.agent.stream_callback import StreamCallbackHandler
from openagent.dto.chat_req import ChatReq

monitoring_cb = LLMonitorCallbackHandler()

session_id = None


@cl.on_chat_start
def start():
    global session_id
    session_id = random().__str__()
    agent = get_agent(session_id)
    # Store the chain in the user session
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message):
    # Retrieve the chain from the user session
    agent = cl.user_session.get("agent")
    msg_type = type(message)
    logger.info(f"message type: {msg_type}")
    if msg_type is Message:
        message = message.content
    cuid = "clnx2bsgi000008l68gxi8q72"
    chat_req_ctx.set(
        ChatReq(
            user_id=cuid,
            message_id=str(uuid.uuid4()),
            type="natural_language",
            body=message,
            session_id=session_id,
        )
    )

    resp_msg_id.set(str(uuid.uuid4()))
    # Call the chain asynchronously
    res = await agent.acall(
        message,
        callbacks=[
            cl.AsyncLangchainCallbackHandler(),
            StreamCallbackHandler(),
            monitoring_cb,
        ],
        metadata={"agentName": "openagent-chainlit", "userId": session_id},
    )

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["output"]).send()
