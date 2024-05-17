from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOllama, ChatOpenAI
from langchain.prompts import PromptTemplate
from loguru import logger

from openagent.conf.env import settings
from openagent.db.database import DBSession
from openagent.db.models import ChatSession

load_dotenv()


async def agen_session_title(user_id: str, session_id: str, history: str) -> list[str]:
    prompt = PromptTemplate(
        template="""
Based on the following user chat history, generate a session title. \
Your response words should less than 10 words and return directly.

History:
{history}
Session Title:
    """,
        input_variables=["history"],
    )
    if settings.MODEL_NAME.startswith("gpt"):
        model = ChatOpenAI(
            model=settings.MODEL_NAME,
            openai_api_base=settings.LLM_API_BASE,
            temperature=0.5,
        )
    else:
        model = ChatOllama(model=settings.MODEL_NAME, base_url=settings.LLM_API_BASE)
    interpreter = LLMChain(llm=model, prompt=prompt)
    logger.info(f"start to generate session title based on history: {history}")
    output = await interpreter.arun(
        history=history,
        metadata={"agentName": "openagent-chainlit", "userId": user_id},
    )
    output = output.strip("'").strip('"')
    logger.info(f"session title generated: {output}")
    with DBSession() as db_session:
        db_session.query(ChatSession).filter(
            ChatSession.session_id == session_id
        ).update({ChatSession.title: output})
        db_session.commit()
    return output
