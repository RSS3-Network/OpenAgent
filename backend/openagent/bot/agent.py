from typing import AsyncIterator

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.schema import StreamEvent
from langchain_openai import ChatOpenAI

from openagent.bot.memory import BotPGMemory
from openagent.experts.article_expert import ArticleExpert
from openagent.experts.feed_expert import FeedExpert
from openagent.experts.nft_expert import NFTExpert
from openagent.experts.price_expert import PriceExpert
from openagent.experts.search_expert import SearchExpert
from openagent.experts.swap_expert import SwapExpert
from openagent.experts.transfer_expert import TransferExpert

load_dotenv()


def get_pg_memory(session_id):
    chat_history = BotPGMemory(
        session_id,
    )
    return chat_history


async def ask(session_id, question) -> AsyncIterator[StreamEvent]:
    agent_with_chat_history = await create_agent()
    events = agent_with_chat_history.astream_events(
        {"input": question},
        version="v1",
        config={"configurable": {"session_id": session_id}},
    )
    return events


async def create_agent():
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    experts = [
        SearchExpert(),
        FeedExpert(),
        PriceExpert(),
        ArticleExpert(),
        NFTExpert(),
        SwapExpert(),
        TransferExpert(),
    ]
    agent = create_tool_calling_agent(
        llm.with_config({"tags": ["agent_llm"]}), experts, prompt
    )
    agent_executor = AgentExecutor(
        agent=agent, tools=experts, verbose=False
    ).with_config({"run_name": "Agent"})
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: get_pg_memory(session_id),
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    return agent_with_chat_history
