from datetime import datetime
from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, Field

from openagent.db.models import ChatSession


class SessionTreeNodeDTOType(str, Enum):
    folder = "folder"
    session = "session"


class SessionTreeNodeDTO(BaseModel):
    session_id: str = Field(description="session id")
    parent_id: str | None = Field(
        example=None, default=None, description="parent id, if null, is root folder"
    )
    title: str | None = Field(default=None, description="session title")
    order: int = Field(
        description="order in parent folder, session will sort by order desc"
    )
    created_at: datetime = Field(description="create time")
    children: list | None = []
    type: SessionTreeNodeDTOType = SessionTreeNodeDTOType.folder

    def __hash__(self):
        return hash(self.session_id) ^ hash(self.type)

    def __lt__(self, other):
        # sort by type , folder first, order asc, created_at desc
        if self.type != other.type:
            return self.type == SessionTreeNodeDTOType.folder
        if self.order != other.order:
            return self.order > other.order
        return self.created_at < other.created_at


def build_session_tree_node(node: ChatSession) -> SessionTreeNodeDTO:
    return SessionTreeNodeDTO(
        session_id=node.session_id,
        title=node.title,
        order=node.order,
        parent_id=node.parent_id,
        created_at=node.created_at,
        type=node.type,
    )


class NewSessionFolderDTO(BaseModel):
    user_id: str = Field(example="jackma")
    title: str = Field(example="folder1")
    order: int = Field(
        example=1, description="order in parent folder, session will sort by order desc"
    )
    parent_id: str | None = Field(
        example=None,
        default=None,
        description="parent id, if null, will create root folder",
    )

    class Config:
        json_schema_extra: ClassVar = {
            "example": {"user_id": "jackma", "title": "folder1", "order": 0}
        }


class SessionTab(str, Enum):
    favorite = "favorite"
    recent = "recent"


class UpdateSessionDTO(BaseModel):
    user_id: str = Field(example="jackma")
    session_id: str = Field(example="1234567890")
    title: str | None = Field(
        example=None,
        default=None,
        description="session title, if null, will not update",
    )
    order: int | None = Field(
        example=None,
        default=None,
        description="session order, if null, will not update",
    )
    tab: SessionTab | None = Field(
        example=None,
        default=None,
        description="session tab, if null, will not update",
    )
    parent_id: str | None = Field(
        example=None,
        default=None,
        description="parent id, if null, will not update",
    )


class MoveSessionDTO(BaseModel):
    user_id: str = Field(description="user id", example="jackma")
    from_session_id: str = Field(description="source session id", example="1234567890")
    to_session_tab: SessionTab = Field(
        description="target tab, favorite or recent. "
        "if recent, to_session_id will be ignored",
        example="favorite",
    )
    to_session_id: str | None = Field(
        description="target parent session id, only valid when"
        " to_session_tab is favorite, if null, "
        "will move to root folder",
        example="0987654321",
        default=None,
    )
