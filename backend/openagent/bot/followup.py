from typing import List

from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from loguru import logger
from sqlalchemy.orm.exc import NoResultFound

from openagent.db.database import DBSession
from openagent.db.models import BotFollowup

load_dotenv()


class FollowUpQuestion(BaseModel):
    questions: List[str] = Field(description="Follow-up questions")


def gen_followup_question(chat_history: List[str]) -> List[str]:
    model = ChatOpenAI(temperature=0.5)
    follow_up_query = "please suggest 5 follow-up questions.\n" f"{chat_history}"
    parser = PydanticOutputParser(pydantic_object=FollowUpQuestion)  # type: ignore

    prompt = PromptTemplate(
        template="You are a web3 OpenAgent."
        "Generate follow-up questions based on the user's chat history."
        "each question should be less than 6 words."
        "\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser
    response = chain.invoke({"query": follow_up_query})
    return response.questions


def store_followup_question(key, question):
    """
    Store follow-up question in the database
    """
    with DBSession() as db_session:
        try:
            # Check if the question already exists
            existing_question = (
                db_session.query(BotFollowup)
                .filter(BotFollowup.key == key)
                .one_or_none()
            )
            if existing_question is None:
                new_followup = BotFollowup(key=key, question=question)
                db_session.add(new_followup)
                db_session.commit()
        except Exception as e:
            logger.error(f"Error storing follow-up question: {e}")
            db_session.rollback()


def get_followup_question(key):
    """
    Retrieve follow-up question from the database using the key
    """
    with DBSession() as db_session:
        try:
            followup_question = (
                db_session.query(BotFollowup).filter(BotFollowup.key == key).one()
            )
            return followup_question.question
        except NoResultFound:
            return None
