from enum import Enum

from pydantic import BaseModel


class CbContentType(str, Enum):
    llm_content = "llm_content"
    tool_content = "tool_content"


class CbToolContent(BaseModel):
    content: object
    tool_name: str


class CbContent(BaseModel):
    type: CbContentType
    content: object
    block_id: str | None = None
