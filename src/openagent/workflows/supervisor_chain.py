from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from loguru import logger

from openagent.conf.llm_provider import get_current_llm
from openagent.workflows.member import members, AgentRole

load_dotenv()


@tool
def route(next_: AgentRole):
    """Select the next role."""
    pass


def build_supervisor_chain():
    system_prompt = """
You are an AI Agent Supervisor coordinating specialized AI Agents. Your task:

1. Analyze user requests and conversation history.
2. Select the most suitable AI Agent based on their expertise:

{members}


Selection principles:
- Match Agent expertise to current needs.
- Prioritize Agents who can advance the task.
- Choose the Agent for the most comprehensive response.

Based on these guidelines, select the next AI Agent or end the conversation.
"""
    members_info = ", ".join([f"{member['name']} ({member['description']})" for member in members])
    system_prompt = system_prompt.format(members=members_info)
    options = [member["name"] for member in members]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),

        ]
    ).partial(options=str(options), members=", ".join([member["name"] for member in members]))
    llm = get_current_llm()

    def extract_next(x):
        try:
            next__ = x[-1]['args']['next_']
        except Exception as ex:
            logger.warning(f"Error extracting next agent: {x}")
            next__ = "fallback_agent"
        return {'next': next__}

    return (
            prompt
            | llm.bind_tools(tools=[route], tool_choice="route")
            | JsonOutputToolsParser()
            | extract_next
    )


