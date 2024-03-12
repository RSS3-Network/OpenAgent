from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from openagent.dto.task import TaskStatus

Base = declarative_base()  # type: ignore


class ChatHistory(Base):  # type: ignore
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False)
    session_id = Column(String(255), nullable=False)
    message_id = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    send_at = Column(DateTime(timezone=True), server_default=func.now())


class ChatSession(Base):  # type: ignore
    __tablename__ = "chat_session"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False)
    session_id = Column(String(255), nullable=False, unique=True)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    parent_id = Column(String(255), nullable=True, default=None)
    order = Column(Integer, nullable=True, default=0)
    type = Column(String(255), nullable=True, default="session")
    tab = Column(String(255), nullable=True, default="recent")


class Task(Base):  # type: ignore
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False)
    session_id = Column(String(255), nullable=False)
    task_id = Column(String(255), nullable=False, unique=True)
    type = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(255), nullable=False, default=TaskStatus.running)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    run_at = Column(DateTime(timezone=True), nullable=True)
    done_at = Column(DateTime(timezone=True), nullable=True)
    hash = Column(String(255), nullable=True)
    is_notified = Column(Boolean, nullable=False, default=False)
