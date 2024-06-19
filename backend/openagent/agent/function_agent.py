from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain_community.chat_models import ChatOllama, ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from toolz import memoize

from openagent.agent.cache import init_cache
from openagent.agent.postgres_history import PostgresChatMessageHistory
from openagent.agent.system_prompt import SYSTEM_PROMPT, custom_agent_kwargs
from openagent.conf.env import settings
from openagent.experts.article_expert import ArticleExpert
from openagent.experts.feed_expert import FeedExpert
from openagent.experts.nft_expert import NFTExpert
from openagent.experts.price_expert import PriceExpert
from openagent.experts.search_expert import SearchExpert
from openagent.experts.swap_expert import SwapExpert
from openagent.experts.transfer_expert import TransferExpert

init_cache()


def create_agent(experts, interpreter, agent_kwargs, memory, agent_type):
    return initialize_agent(
        experts,
        interpreter,
        agent=agent_type,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
        handle_parsing_errors=True,
    )


def create_interpreter(model_name):
    if model_name.startswith("gpt"):
        return ChatOpenAI(
            model=model_name,
            openai_api_base=settings.LLM_API_BASE,
            temperature=0.3,
            streaming=True,
        )
    elif model_name.startswith("gemini"):
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=settings.GOOGLE_API_KEY,
        )
    else:
        return ChatOllama(
            model=model_name,
            base_url=settings.LLM_API_BASE,
        )


@memoize
def get_agent(session_id: str) -> AgentExecutor:
    # Initialize message history based on session_id
    message_history = (
        get_msg_history(session_id) if session_id else ChatMessageHistory()
    )

    # Define agent arguments
    agent_kwargs = (
        {
            "system_message": SystemMessage(content=SYSTEM_PROMPT),
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        }
        if settings.MODEL_NAME.startswith("gpt")
        else custom_agent_kwargs
    )

    # Create conversation memory
    memory = ConversationBufferMemory(
        memory_key="memory", return_messages=True, chat_memory=message_history
    )

    # List of experts to be loaded
    experts = [
        SearchExpert(),
        FeedExpert(),
        PriceExpert(),
        ArticleExpert(),
        NFTExpert(),
        SwapExpert(),
        TransferExpert(),
    ]

    # Initialize interpreter
    interpreter = create_interpreter(settings.MODEL_NAME)

    # Define agent type based on model name
    agent_type = (
        AgentType.OPENAI_FUNCTIONS
        if settings.MODEL_NAME.startswith("gpt")
        else AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
    )

    # Return created agent with appropriate arguments
    return create_agent(experts, interpreter, agent_kwargs, memory, agent_type)


# this function is used to get the chat history of a session from Postgres
def get_msg_history(session_id):
    return PostgresChatMessageHistory(
        session_id=session_id,
    )
