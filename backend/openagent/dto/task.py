import json
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TransferDTO(BaseModel):
    user_id: str = Field(description="user id", example="clnx2bsgi000008l68gxi8q72")
    task_id: str = Field(description="task id", example="1")
    executor_id: int = Field(description="executor id", example=1)
    to_address: str = Field(
        description="address to transfer",
        example="0xFcf62726dbf3a9C2765f138111AA04Bf50bD67D6",
    )
    amount: str = Field(description="amount to transfer", example="0.001")
    token_address: str = Field(
        description="token address",
        example="0x4d2bf3A34a2311dB4b3D20D4719209EDaDBf69b6",
    )
    token: str = Field(description="token", example="ETH")
    logoURI: str
    decimals: int


class ConfirmTransferDTO(BaseModel):
    user_id: str = Field(description="user id", example="clnx2bsgi000008l68gxi8q72")
    task_id: str = Field(description="task id", example="1")
    executor_id: int = Field(description="executor id", example=1)
    to_address: str = Field(
        description="address to transfer",
        example="0xFcf62726dbf3a9C2765f138111AA04Bf50bD67D6",
    )
    amount: str = Field(description="amount to transfer", example="0.001")
    token_address: str = Field(
        description="token address",
        example="0x4d2bf3A34a2311dB4b3D20D4719209EDaDBf69b6",
    )


class CancelTransferDTO(BaseModel):
    user_id: str = Field(description="user id", example="clnx2bsgi000008l68gxi8q72")
    task_id: str = Field(description="task id", example="1")


class TransferQueryDTO(BaseModel):
    executor_id: int = Field(description="executor id", example=1)
    to_address: str = Field(
        description="address to transfer",
        example="0xFcf62726dbf3a9C2765f138111AA04Bf50bD67D6",
    )
    amount: str = Field(description="amount to transfer", example="0.001")
    token_address: str = Field(
        description="token address",
        example="0x4d2bf3A34a2311dB4b3D20D4719209EDaDBf69b6",
    )
    token: str = Field(description="token", example="ETH")
    logoURI: str | None = Field(
        description="logo uri", example="https://li.quest/logo.png"
    )
    decimals: int | None = Field(description="decimals", example=18)


class TaskStatus(str, Enum):
    idle = "idle"
    pending = "pending"
    running = "running"
    done = "done"
    canceled = "canceled"
    failed = "failed"


class TaskType(str, Enum):
    transfer = "transfer"
    # swap = "swap"


class TaskDTO(BaseModel):
    task_id: str
    user_id: str
    session_id: str
    type: TaskType
    body: TransferQueryDTO | object = None
    status: TaskStatus
    created_at: datetime
    hash: str | None = None
    run_at: datetime | None = None
    done_at: datetime | None = None


def build_task_dto(task):
    body = json.loads(task.body)
    return TaskDTO(
        task_id=task.task_id,
        user_id=task.user_id,
        session_id=task.session_id,
        type=task.type,
        body=body,
        status=task.status,
        created_at=task.created_at,
        hash=task.hash,
        run_at=task.run_at,
        done_at=task.done_at,
    )
