"""Client for persisting chat message history in a Postgres database.

This client provides support for both sync and async via psycopg 3.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict

from openagent.db.database import DBSession
from openagent.db.models import BotMsg

logger = logging.getLogger(__name__)


class BotPGMemory(BaseChatMessageHistory):
    def __init__(
        self,
        session_id: str,
    ) -> None:
        self._session_id = session_id
        self._db_session = DBSession()

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """Add messages to the chat message history."""

        values = [
            BotMsg(
                session_id=self._session_id,
                msg=json.dumps(message_to_dict(message)),
                send_at=datetime.now(),
            )
            for message in messages
        ]

        self._db_session.add_all(values)
        self._db_session.commit()

    async def aadd_messages(self, messages: Sequence[BaseMessage]) -> None:
        self.add_messages(messages)

    def get_messages(self) -> list[BaseMessage]:
        """Retrieve messages from the chat message history."""
        items = list(
            map(
                lambda x: json.loads(x.msg),
                self._db_session.query(BotMsg)
                .filter(BotMsg.session_id == self._session_id)
                .order_by(BotMsg.send_at.asc())
                .all(),
            )
        )

        messages = messages_from_dict(items)
        return messages

    async def aget_messages(self) -> list[BaseMessage]:
        """Retrieve messages from the chat message history."""

        return self.get_messages()

    @property  # type: ignore[override]
    def messages(self) -> list[BaseMessage]:
        """The abstraction required a property."""
        return self.get_messages()

    def clear(self) -> None:
        """Clear the chat message history for the GIVEN session."""
        pass

    async def aclear(self) -> None:
        pass
