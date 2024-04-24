from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.chat_models import ChatOllama, ChatOpenAI
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from toolz import memoize

from openagent.agent.cache import init_cache
from openagent.agent.postgres_history import PostgresChatMessageHistory
from openagent.agent.system_prompt import SYSTEM_PROMPT, ollama_agent_kwargs
from openagent.conf.env import settings
from openagent.experts.account_expert import AccountExpert
from openagent.experts.collection_expert import CollectionExpert
from openagent.experts.feed_expert import FeedExpert
from openagent.experts.google_expert import GoogleExpert
from openagent.experts.hoot_expert import HootExpert
from openagent.experts.swap_expert import SwapExpert
from openagent.experts.transfer_expert import TransferExpert

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
    # load Experts as tools for the agent
    experts = [
        GoogleExpert(),
        FeedExpert(),
        CollectionExpert(),
        AccountExpert(),
        SwapExpert(),
        TransferExpert(),
        HootExpert(),
    ]

    if settings.MODEL_NAME.startswith("gpt"):
        interpreter = ChatOpenAI(
            model=settings.MODEL_NAME,
            openai_api_base=settings.LLM_API_BASE,
            temperature=0.3,
            streaming=True,
        )
        return initialize_agent(
            experts,
            interpreter,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            agent_kwargs=agent_kwargs,
            memory=memory,
            handle_parsing_errors=True,
        )
    else:
        interpreter = ChatOllama(
            model=settings.MODEL_NAME,
            base_url=settings.LLM_API_BASE,
        )
        return initialize_agent(
            experts,
            interpreter,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs=ollama_agent_kwargs,
            memory=memory,
            handle_parsing_errors=True,
        )


# this function is used to get the chat history of a session from Postgres
def get_msg_history(session_id):
    return PostgresChatMessageHistory(
        session_id=session_id,
    )
