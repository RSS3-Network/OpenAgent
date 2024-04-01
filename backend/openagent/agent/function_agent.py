from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI, ChatOllama
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from toolz import memoize

from openagent.agent.cache import init_cache
from openagent.agent.postgres_history import PostgresChatMessageHistory
from openagent.agent.system_prompt import SYSTEM_PROMPT
from openagent.conf.env import settings
from openagent.experts.account_expert import AccountExpert
from openagent.experts.collection_expert import CollectionExpert
from openagent.experts.dapp_expert import DappExpert
from openagent.experts.executor_expert import ExecutorExpert
from openagent.experts.feed_expert import FeedExpert
from openagent.experts.google_expert import GoogleExpert
from openagent.experts.network_expert import NetworkExpert
from openagent.experts.swap_expert import SwapExpert
from openagent.experts.token_expert import TokenExpert
from openagent.experts.transfer_expert import TransferExpert

init_cache()


@memoize
def get_agent(session_id: str) -> AgentExecutor:
    message_history = (
        get_msg_history(session_id) if session_id else ChatMessageHistory()
    )
    agent_kwargs = {
        "prefix": """
Your designated name is RSS3 Node Assistant, developed by RSS3, \
you have the capability to call upon tools to aid in answering questions.

Assistants may prompt the user to employ specific tools to gather information that might be helpful in addressing the user's initial question.

Here are tools' schemas:
        """,
        "format_instructions": """

When responding, you must exclusively use one of the following two formats:

**Option 1:**
If you're suggesting that the user utilizes a tool, format your response as a markdown code snippet according to this schema:

```json
{{{{
    "action": string, // The action to be taken. Must be one of {tool_names}
    "action_input": object  // The parameters for the action. MUST be JSON object
}}}}
```

**Option #2:**
If you're providing a direct response to the user, format your response as a markdown code snippet following this schema:

```json
{{{{
    "action": "Final Answer", // MUST be literal string "Final Answer", other forms are not acceptable
    "action_input": string // This should contain your response to the user, in human-readable language
}}}}
```

"action\_input" is illegal, never escape it with a backslash. 
""",
        "suffix": """
REMEMBER to respond with a markdown code snippet of a json \
blob with a single action, and NOTHING else""",
    }
    memory = ConversationBufferMemory(
        memory_key="memory", return_messages=True, chat_memory=message_history
    )
    model = ChatOllama(model=settings.MODEL_NAME, base_url=settings.MODEL_BASE_URL)

    # load Exports as tools for the agent
    tools = [
        # GoogleExpert(),
        NetworkExpert(),
        FeedExpert(),
        CollectionExpert(),
        TokenExpert(),
        DappExpert(),
        # AccountExpert(),
        # SwapExpert(),
        # TransferExpert(),
        # ExecutorExpert(),
    ]
    return initialize_agent(
        tools,
        model,
        # AgentType.OPENAI_FUNCTIONS is tested to be the most performant
        # thus local LLM must be conformed to this type
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
        handle_parsing_errors=True,
    )


# this function is used to get the chat history of a session from Postgres
def get_msg_history(session_id):
    return PostgresChatMessageHistory(
        session_id=session_id,
    )
