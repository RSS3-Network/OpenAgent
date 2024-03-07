import json
import logging
from typing import List

from langchain.schema import (
    BaseChatMessageHistory,
)
from langchain.schema.messages import BaseMessage, messages_from_dict

from copilot.db.database import DBSession
from copilot.db.models import ChatHistory
from toolz.curried import compose_left, map, filter

logger = logging.getLogger(__name__)


class PostgresChatMessageHistory(BaseChatMessageHistory):
    """Chat message history stored in a Postgres database."""

    def __init__(
        self,
        session_id: str,
    ):
        self.session_id = session_id

    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        with DBSession() as db_session:
            histories = (
                db_session.query(ChatHistory)
                .filter(ChatHistory.session_id == self.session_id)
                .all()
            )
            lst = compose_left(
                map(compose_left(lambda x: x.message, json.loads)),
                filter(lambda x: x["type"] in ["ai", "human"]),
                list,
            )(histories)
            return messages_from_dict(lst)

    def add_message(self, message: BaseMessage) -> None:
        # saved by stream callback
        pass

    def clear(self) -> None:
        ChatHistory.filter(session_id=self.session_id).delete()

    def __del__(self) -> None:
        pass
