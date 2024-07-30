import ollama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

from openagent.conf.llm_provider import get_current_llm


def fallback(state):
    logger.info("Running fallback agent")

    chat_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are openagent!

Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
            """,
            ),
            *state["messages"][0:-1],
            ("human", "{input}"),
        ]
    )
    chain = chat_template | chat_template | get_current_llm() | StrOutputParser()
    return {
        "messages": [
            HumanMessage(
                content=chain.invoke({"input": state["messages"][-1].content}),
                name="fallback",
            )
        ]
    }

