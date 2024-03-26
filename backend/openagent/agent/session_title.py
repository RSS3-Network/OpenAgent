from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI, ChatOllama
from langchain.prompts import PromptTemplate
from loguru import logger

from openagent.db.database import DBSession
from openagent.db.models import ChatSession
from openagent.conf.env import settings

load_dotenv()


async def agen_session_title(
    user_id: str, session_id: str, history: str
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
    model = ChatOllama(model=settings.MODEL_NAME, base_url=settings.MODEL_BASE_URL)
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


if __name__ == '__main__':

    import asyncio
    asyncio.run(agen_session_title("123","456","what's your name ?"))