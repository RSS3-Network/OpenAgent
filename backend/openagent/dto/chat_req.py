from enum import Enum

from pydantic import BaseModel, Field


class ChatReqType(str, Enum):
    natural_language = "natural_language"
    order_placement_request = "order_placement_request"


class ChatReq(BaseModel):
    session_id: str = Field(example="1234567890")
    message_id: str = Field(example="1234567890")
    user_id: str = Field(example="clnx2bsgi000008l68gxi8q72")
    type: ChatReqType = Field(example="natural_language")
    body: str = Field(example="transfer 0.001 ct to vitalik.eth")
