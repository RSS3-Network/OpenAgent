from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from loguru import logger

from copilot.db.database import DBSession
from copilot.db.models import ChatSession
from copilot.conf.env import settings

load_dotenv()


async def agen_session_title(
    user_id: str, session_id: str, history: str, monitoring_cb
) -> list[str]:
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

    model = ChatOpenAI(openai_api_base=settings.API_BASE, temperature=0.5)
    chain = LLMChain(llm=model, prompt=prompt)
    logger.info(f"start to generate session title based on history: {history}")
    output = await chain.arun(
        history=history,
        callbacks=[monitoring_cb],
        metadata={"agentName": "copilot-chainlit", "userId": user_id},
    )
    output = output.strip("'").strip('"')
    logger.info(f"session title generated: {output}")
    with DBSession() as db_session:
        db_session.query(ChatSession).filter(
            ChatSession.session_id == session_id
        ).update({ChatSession.title: output})
        db_session.commit()
    return output
