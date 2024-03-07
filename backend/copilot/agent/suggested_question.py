from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from loguru import logger

from copilot.conf.env import settings

load_dotenv()


async def agen_suggested_questions(
    user_id: str, history: str, monitoring_cb
) -> list[str]:
    prompt = PromptTemplate(
        template="""
Based on the following user chat history, \
generate 3-5 suggested questions that the user may be interested in asking next round.
The suggested questions can explore new topics, but should be relevant to the user's interests.
Your response should be a list of strings.

Example:

History:
eth price?
Suggested Questions:
What is the price of BTC? \n What is ETH? \n Can you list some hot tokens on Ethereum? \n

History:
{history}
Suggested Questions:
    """,
        input_variables=["history"],
    )

    model = ChatOpenAI(openai_api_base=settings.API_BASE, temperature=0.5)
    chain = LLMChain(llm=model, prompt=prompt)
    logger.info(f"start to generate suggested questions based on history: {history}")
    output = await chain.arun(
        history=history,
        callbacks=[monitoring_cb],
        metadata={"agentName": "copilot-chainlit", "userId": user_id},
    )
    logger.info(f"suggested questions generated: {output}")
    return output.split("\n")
