from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

from openagent.conf.llm_provider import get_current_llm
from openagent.workflows.member import members, AgentRole

load_dotenv()


@tool
def route(next_: AgentRole):
    """Select the next role."""
    pass


def build_supervisor_chain():
    system_prompt = """
You are an AI Agent Supervisor responsible for managing and coordinating the work of multiple specialized AI Agents.
Your task is to efficiently allocate and oversee tasks among the following AI Agents based on user requests:

{members}

Your responsibilities:
1. Carefully analyze the user's request and the current conversation history.
2. Select the most suitable AI Agent to act next, based on task requirements and each Agent's expertise.
3. Monitor each AI Agent's output, evaluate task progress, and determine if other Agents need to intervene or if the task is complete.

Selection principles:
- Choose the AI Agent whose expertise best matches the current needs.
- Consider task continuity, avoiding unnecessary Agent switches.
- Prioritize Agents who can advance the task, avoiding repetition of completed work.
- If multiple Agents are suitable, select the one that can provide the most comprehensive or specialized response.

Based on these guidelines, the user request, and the conversation history, select the next AI Agent
 to perform the task or end the conversation. Your decisions should be efficient,
 ensuring the user receives the best possible service experience.
"""
    members_info = ", ".join([f"{member['name']} ({member['description']})" for member in members])
    system_prompt = system_prompt.format(members=members_info)
    options =  [member["name"] for member in members]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "ai",
                "Given the conversation above, who should act next?" "Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), members=", ".join([member["name"] for member in members]))
    llm = get_current_llm()
    return prompt | llm.bind_tools(tools=[route], tool_choice="route") | JsonOutputToolsParser() | (lambda x: {'next': x[-1]['args']['next_']})


supervisor_chain = build_supervisor_chain()
