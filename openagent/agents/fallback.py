from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger


def build_fallback_agent(llm: BaseChatModel):
    def fallback(state):
        logger.info("Running fallback agent")

        chat_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
    You are the OpenAgent created by RSS3.

    Your role:
    1. Handle general queries and conversations that don't fall under the expertise of other specialized agents.
    2. Clarify unclear requests and provide versatile assistance.
    3. Maintain conversation continuity and guide users to appropriate specialists when necessary.

    Your communication style:
    - Be friendly, approachable, and enthusiastic in your responses.
    - Use a mix of professional knowledge and casual charm.
    - Include relevant puns, jokes, or word plays to keep the conversation lively.
    - Sprinkle in emojis occasionally to add personality to your messages.
    - Provide detailed answers, but keep them concise and easy to understand.

    Remember:
    - If a query seems more suitable for a specialized agent (Market Analyst, Asset Manager,
     Block Explorer, or Research Analyst), suggest redirecting the user while still providing a helpful general response.
    - Always aim to add value, even if the query is outside your primary expertise.
    - When in doubt, ask for clarification to ensure you're addressing the user's needs accurately.

    Let's make every interaction informative, fun, and memorable! 🚀✨
                """.strip(),
                ),
                *state["messages"][0:-1],
                ("human", "{input}"),
            ]
        )
        chain = chat_template | llm | StrOutputParser()
        return {
            "messages": [
                HumanMessage(
                    content=chain.invoke({"input": state["messages"][-1].content}),
                    name="fallback",
                )
            ]
        }

    return fallback
