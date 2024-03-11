from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from toolz import memoize

from openagent.agent.cache import init_cache
from openagent.agent.postgres_history import PostgresChatMessageHistory
from openagent.agent.system_prompt import SYSTEM_PROMPT
from openagent.experts.feed_tool import FeedTool
from openagent.experts.google_tool import GoogleTool
from openagent.experts.network_tool import NetworkTool
from openagent.experts.collection_tool import CollectionTool
from openagent.experts.token_tool import TokenTool
from openagent.experts.dapp_tool import DappTool
from openagent.experts.account_tool import AccountTool
from openagent.experts.swap_tool import SwapTool
from openagent.experts.transfer_tool import TransferTool
from openagent.experts.wallet_tool import WalletTool
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
        GoogleTool(),
        NetworkTool(),
        FeedTool(),
        CollectionTool(),
        TokenTool(),
        DappTool(),
        AccountTool(),
        SwapTool(),
        TransferTool(),
        WalletTool(),
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
