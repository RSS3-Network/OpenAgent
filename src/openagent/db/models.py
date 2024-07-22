import uuid

from sqlalchemy import ARRAY, JSON, Boolean, Column, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # type: ignore


class User(Base):  # type: ignore
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifier = Column(Text, nullable=False, unique=True)
    metadata_ = Column("metadata", JSON, nullable=False)
    createdAt = Column(Text)


class Thread(Base):  # type: ignore
    __tablename__ = "threads"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    createdAt = Column(Text)
    name = Column(Text)
    userId = Column(UUID(as_uuid=True))
    userIdentifier = Column(Text)
    tags = Column(ARRAY(Text))  # type: ignore
    metadata_ = Column("metadata", JSON)


class Step(Base):  # type: ignore
    __tablename__ = "steps"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    threadId = Column(UUID(as_uuid=True))
    parentId = Column(UUID(as_uuid=True))
    disableFeedback = Column(Boolean, nullable=False)
    streaming = Column(Boolean, nullable=False)
    waitForAnswer = Column(Boolean)
    isError = Column(Boolean)
    metadata_ = Column("metadata", JSON)
    tags = Column(ARRAY(Text))  # type: ignore
    input = Column(Text)
    output = Column(Text)
    createdAt = Column(Text)
    start = Column(Text)
    end = Column(Text)
    generation = Column(JSON)
    showInput = Column(Text)
    language = Column(Text)
    indent = Column(Integer)


class Element(Base):  # type: ignore
    __tablename__ = "elements"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threadId = Column(UUID(as_uuid=True))
    type = Column(Text)
    url = Column(Text)
    chainlitKey = Column(Text)
    name = Column(Text, nullable=False)
    display = Column(Text)
    objectKey = Column(Text)
    size = Column(Text)
    page = Column(Integer)
    language = Column(Text)
    forId = Column(UUID(as_uuid=True))
    mime = Column(Text)


class Feedback(Base):  # type: ignore
    __tablename__ = "feedbacks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forId = Column(UUID(as_uuid=True), nullable=False)
    value = Column(Integer, nullable=False)
    comment = Column(Text)
    threadId = Column(UUID(as_uuid=True))
