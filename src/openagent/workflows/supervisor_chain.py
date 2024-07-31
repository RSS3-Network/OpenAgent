from dotenv import load_dotenv
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from openagent.conf.llm_provider import get_current_llm
from openagent.workflows.member import members

load_dotenv()


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

Completion criteria:
- Select FINISH when all user requests have been satisfactorily addressed.
- Choose FINISH if an AI Agent explicitly states that the task is fully completed.
- Opt for FINISH if you determine no more Agents can provide valuable input for the current task.

Based on these guidelines, the user request, and the conversation history, select the next AI Agent
 to perform the task or end the conversation. Your decisions should be efficient,
 ensuring the user receives the best possible service experience.
"""
    members_info = ", ".join([f"{member['name']} ({member['description']})" for member in members])
    system_prompt = system_prompt.format(members=members_info)
    options = ["FINISH"] + [member["name"] for member in members]
    function_def = {
        "name": "route",
        "description": "Select the next role.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [
                        {"enum": options},
                    ],
                }
            },
            "required": ["next"],
        },
    }
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?" " Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), members=", ".join([member["name"] for member in members]))
    llm = get_current_llm()
    return prompt | llm.bind_functions(functions=[function_def],
                                       function_call="route") | JsonOutputFunctionsParser()


supervisor_chain = build_supervisor_chain()
