from enum import Enum

from pydantic import BaseModel


class ChatRespType(str, Enum):
    natural_language = "natural_language"
    order_placement_inquiry = "order_placement_inquiry"
    suggested_questions = "suggested_questions"
    session_title = "session_title"
    tool = "tool"
    error = "error"


class ChatResp(BaseModel):
    message_id: str | None
    block_id: str | None = None
    type: ChatRespType
    body: object
