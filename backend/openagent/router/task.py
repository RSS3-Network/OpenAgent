from fastapi import APIRouter, Query
from loguru import logger
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.websockets import WebSocket, WebSocketDisconnect

from openagent.dto.error import ErrorResp
from openagent.dto.task import (
    TaskStatus,
    TaskDTO,
    CancelTransferDTO,
    ConfirmTransferDTO,
)
from openagent.service import task
from openagent.service.task import user2ws

task_router = APIRouter(tags=["Task"])


@task_router.websocket("/tasks/notifications/{user_id}")
async def get_notifications(user_id: str, websocket: WebSocket):
    await websocket.accept()
    user2ws[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        del user2ws[user_id]


@task_router.get("/tasks/query_list", response_model=list[TaskDTO])
async def query_list(
    user_id: str = Query(example="clnx2bsgi000008l68gxi8q72"),
    session_id: str | None = None,
    status: TaskStatus | None = None,
    offset: int = 0,
    limit: int = 50,
):
    return task.query_list(user_id, session_id, status, offset, limit)


@task_router.post("/tasks/confirm_transfer")
async def confirm_transfer(req: ConfirmTransferDTO):
    logger.info(f"Received request: {req}")
    try:
        return await task.transfer(req)
    except Exception as e:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content=ErrorResp(code=400, message=e.__str__()).dict(),
        )


@task_router.post("/tasks/cancel_task")
async def cancel_task(req: CancelTransferDTO):
    user_id = req.user_id
    task_id = req.task_id
    logger.info(f"Received request: user_id: {user_id}, task_id: {task_id}")
    try:
        return await task.cancel_task(user_id, task_id)
    except Exception as e:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content=ErrorResp(code=400, message=e.__str__()).dict(),
        )


@task_router.get("/tasks/fetch_one_task")
async def fetch_one_task(
    user_id: str = Query(example="clnx2bsgi000008l68gxi8q72"),
    task_id: str = Query(example="1"),
):
    logger.info(f"Received request: user_id: {user_id}, task_id: {task_id}")
    try:
        id_ = await task.fetch_one_task(user_id, task_id)
        return id_
    except Exception as e:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content=ErrorResp(code=400, message=e.__str__()).dict(),
        )
