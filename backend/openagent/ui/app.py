import chainlit as cl
from chainlit.types import ThreadDict
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable.config import RunnableConfig

from openagent.agent.function_agent import get_agent


def setup_runnable():
    agent = get_agent("")
    cl.user_session.set("runnable", agent)


# @cl.oauth_callback
# def oauth_callback(
#     provider_id: str,
#     token: str,
#     raw_user_data: Dict[str, str],
#     default_user: cl.User,
# ) -> Optional[cl.User]:
#     return default_user
#


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))
    setup_runnable()


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    memory = ConversationBufferMemory(return_messages=True)
    root_messages = [m for m in thread["steps"]]
    for message in root_messages:
        if message["type"] == "user_message":
            memory.chat_memory.add_user_message(message["output"])
        else:
            memory.chat_memory.add_ai_message(message["output"])

    cl.user_session.set("memory", memory)

    setup_runnable()


@cl.on_message
async def on_message(message: cl.Message):
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory

    runnable = cl.user_session.get("runnable")

    res = cl.Message(content="")

    result = await runnable.ainvoke(
        {"input": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    )

    await cl.Message(content=result["output"]).send()

    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(res.content)


if __name__ == "__main__":
    from chainlit.cli import run_chainlit

    run_chainlit(__file__)
