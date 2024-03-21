import json
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from toolz.curried import groupby

from openagent.dto.chat_req import ChatReqType
from openagent.dto.chat_resp import ChatRespType


class ChatSession(BaseModel):  # type: ignore
    session_id: str
    title: str | None

    @classmethod
    def from_orm(cls, obj):
        return ChatSession(
            session_id=obj.session_id,
            title=obj.title,
        )


class ChatMessageRole(str, Enum):
    ai = "ai"
    human = "human"

    @classmethod
    def from_type(cls, type0: str):
        if type0 == "ai":
            return ChatMessageRole.ai
        if type0 == "human":
            return ChatMessageRole.human
        if type0 in ["tool"]:
            return ChatMessageRole.ai
        raise ValueError(f"Unknown role: {type0}")


class ChatMessageContent(BaseModel):  # type: ignore
    type: ChatRespType | ChatReqType
    block_id: str | None = None
    body: object


class ChatMessage(BaseModel):  # type: ignore
    message_id: str
    role: ChatMessageRole
    content: list[ChatMessageContent]
    send_at: datetime

    @classmethod
    def from_orm(cls, entities):
        msg_id2msgs = groupby(lambda x: x.message_id, entities)

        res = []
        skip_msg_ids = set()
        for entity in entities:
            if entity.message_id in skip_msg_ids:
                continue
            else:
                skip_msg_ids.add(entity.message_id)
            msgs = msg_id2msgs[entity.message_id]
            first_msg = msgs[0]
            first_msg_json = json.loads(first_msg.message)
            contents = []
            for msg in msgs:
                msg_type = None
                msg_json = json.loads(msg.message)
                lc_msg_type = msg_json["type"]
                if lc_msg_type in ["ai", "human"]:
                    msg_type = "natural_language"
                if lc_msg_type in ["tool"]:
                    msg_type = "tool"

                block_id = msg_json["data"]["additional_kwargs"]["block_id"]

                contents.append(
                    ChatMessageContent(
                        block_id=block_id,
                        type=msg_type,
                        body=to_json(msg_json["data"]["content"]),
                    )
                )

            # reverse the order of contents
            contents = contents[::-1]
            res.append(
                ChatMessage(
                    message_id=first_msg.message_id,
                    role=ChatMessageRole.from_type(first_msg_json["type"]),
                    content=contents,
                    send_at=first_msg.send_at,
                )
            )

        return res


def to_json(obj):
    try:
        return json.loads(obj)
    except Exception:
        return obj


class ChatHistory(BaseModel):
    title: str | None
    messages: list[ChatMessage]
