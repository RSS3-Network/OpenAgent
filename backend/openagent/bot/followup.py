from typing import List, Optional

from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from loguru import logger
from sqlalchemy.orm.exc import NoResultFound

from openagent.db.database import DBSession
from openagent.db.models import BotFollowup

load_dotenv()


class FollowUpQuestion(BaseModel):
    questions: List[str] = Field(description="List of follow-up questions")


def gen_followup_question(chat_history: List[str]) -> List[str]:
    """
    Generate follow-up questions based on the chat history.

    :param chat_history: List of chat history strings.
    :return: List of follow-up questions.
    """
    model = ChatOpenAI(temperature=0.3)
    follow_up_query = "please suggest 5 follow-up questions.\n" f"{chat_history}"
    parser = PydanticOutputParser(pydantic_object=FollowUpQuestion)  # type: ignore
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are OpenAgent, a professional Web3 domain chatbot assistant. \
You have the following capabilities:
1. Query historical transaction activities of Ethereum addresses
2. Fetch real-time market prices of various cryptocurrencies
3. Provide information about popular NFT projects
4. Search for fundamental information on specific cryptocurrencies
Conversation Requirements:
1. Based on the user's previous chat content, predict the short \
questions they might ask next
2. If the previous conversation is not related to Web3, skillfully \
guide the topic into the Web3 domain
3. Generated questions should avoid repetition, be limited to 5 \
words, and take the user's perspective
Example Questions:
- What's vitalik.eth up to?
- Current ETH price?
- Hottest NFT projects?

{format_instructions}
""",
            ),
            ("human", "{query}"),
        ]
    )

    chain = prompt | model | parser
    response = chain.invoke(
        {
            "query": follow_up_query,
            "format_instructions": parser.get_format_instructions(),
        }
    )
    return response.questions


def store_followup_question(key: str, question: str) -> None:
    """
    Store a follow-up question in the database.

    :param key: Unique key for the follow-up question.
    :param question: The follow-up question to store.
    """
    with DBSession() as db_session:
        try:
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
            logger.error(f"Error while storing follow-up question: {e}")
            db_session.rollback()


def get_followup_question(key: str) -> Optional[str]:
    """
    Retrieve a follow-up question from the database using the key.

    :param key: Unique key for the follow-up question.
    :return: The follow-up question if found, otherwise None.
    """
    with DBSession() as db_session:
        try:
            followup_question = (
                db_session.query(BotFollowup).filter(BotFollowup.key == key).one()
            )
            return str(followup_question.question)
        except NoResultFound:
            return None
