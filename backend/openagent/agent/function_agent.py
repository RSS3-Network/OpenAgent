from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from toolz import memoize

from openagent.agent.cache import init_cache
from openagent.agent.postgres_history import PostgresChatMessageHistory
from openagent.agent.system_prompt import SYSTEM_PROMPT
from openagent.experts.feed_expert import FeedExpert
from openagent.experts.google_expert import GoogleExpert
from openagent.experts.network_expert import NetworkExpert
from openagent.experts.collection_expert import CollectionExpert
from openagent.experts.token_expert import TokenExpert
from openagent.experts.dapp_expert import DappExpert
from openagent.experts.account_expert import AccountExpert
from openagent.experts.swap_expert import SwapExpert
from openagent.experts.transfer_expert import TransferExpert
from openagent.experts.executor_expert import ExecutorExpert
from openagent.conf.env import settings

init_cache()


@memoize
def get_agent(session_id: str) -> AgentExecutor:
    message_history = (
        get_msg_history(session_id) if session_id else ChatMessageHistory()
    )
    agent_kwargs = {
        "system_message": SystemMessage(content=SYSTEM_PROMPT),
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    memory = ConversationBufferMemory(
        memory_key="memory", return_messages=True, chat_memory=message_history
    )
    interpreter = ChatOpenAI(
        openai_api_base=settings.API_BASE,
        temperature=0.3,
        streaming=True,
    )
    tools = [
        GoogleExpert(),
        NetworkExpert(),
        FeedExpert(),
        CollectionExpert(),
        TokenExpert(),
        DappExpert(),
        AccountExpert(),
        SwapExpert(),
        TransferExpert(),
        ExecutorExpert(),
    ]
    return initialize_agent(
        tools,
        interpreter,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
        handle_parsing_errors=True,
    )


def get_msg_history(session_id):
    return PostgresChatMessageHistory(
        session_id=session_id,
    )
