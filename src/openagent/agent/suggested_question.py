import json

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI
from loguru import logger

from openagent.conf.env import settings

load_dotenv()


async def agen_suggested_questions(user_id: str, history: str) -> list[str]:
    prompt = PromptTemplate(
        template="""
Suggest follow up questions based on the user chat history.

Return Format:
["question1", "question2", "question3"]

Example:

Q:
eth price?
A:
["What is the price of BTC?", "What is ETH?", "Can you list some hot tokens on Ethereum?"]

Q:
what is the price of BTC?
A:
["What is the price of ETH?", "What is the price of BTC?", "Can you list some hot tokens on Ethereum?"]

-----------------------------------------------------------------
Q:
{history}
A:""",
        input_variables=["history"],
    )
    if settings.MODEL_NAME.startswith("gpt"):
        model = ChatOpenAI(
            model=settings.MODEL_NAME,
            openai_api_base=settings.LLM_API_BASE,
            temperature=0.5,
        )
    elif settings.MODEL_NAME.startswith("gemini"):
        if settings.GOOGLE_GEMINI_API_KEY is not None:
            model = ChatGoogleGenerativeAI(model=settings.MODEL_NAME, google_api_key=settings.GOOGLE_GEMINI_API_KEY, temperature=0.5)
        else:
            model = ChatVertexAI(model_name=settings.MODEL_NAME, project=settings.GOOGLE_CLOUD_PROJECT_ID, temperature=0.5)
    else:
        model = ChatOllama(model=settings.MODEL_NAME, base_url=settings.LLM_API_BASE)
    interpreter = LLMChain(llm=model, prompt=prompt)
    logger.info(f"start to generate suggested questions based on history: {history}")
    output = await interpreter.arun(
        history=history,
    )
    logger.info(f"suggested questions generated: {output}")
    # parse output, it's json array str
    lst = json.loads(output)
    logger.info(f"suggested questions parsed: {lst}")
    return lst
