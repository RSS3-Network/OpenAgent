from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import NoResultFound
from starlette import status

from openagent.dto.chat_history import ChatHistory, ChatSession
from openagent.dto.error import ErrorResp
from openagent.dto.session import (
    NewSessionFolderDTO,
    SessionTreeNodeDTO,
    UpdateSessionDTO,
)
from openagent.service.history import (
    delete_histories,
    get_histories,
)
from openagent.service.history import get_recent_sessions as get_recent_sessions0
from openagent.service.session import (
    create_session_folder as create_session_folder0,
)
from openagent.service.session import (
    get_session_tree as get_session_tree0,
)
from openagent.service.session import (
    update_session as update_session0,
)

session_router = APIRouter(tags=["Session"])


@session_router.get("/sessions/tab/recent", response_model=list[ChatSession])
async def get_recent_sessions(user_id: str = Query(example="jackma"), offset: int = 0, limit: int = 50) -> list[str]:
    logger.info(f"Received request: user_id={user_id}, offset={offset}, limit={limit}")
    return get_recent_sessions0(user_id, offset, limit)


@session_router.get("/sessions/tab/favorites", response_model=list[SessionTreeNodeDTO])
async def get_favorite_session_tree(user_id: str = Query(example="jackma")):
    logger.info(f"Received request: user_id={user_id}")
    return get_session_tree0(user_id)


@session_router.get("/sessions/{user_id}/{session_id}", response_model=ChatHistory | ErrorResp)
async def get_session_chat_history(user_id: str, session_id: str, offset: int = 0, limit: int = 50):
    logger.info(
        f"Received request: user_id={user_id}, session_id={session_id},\
offset={offset}, limit={limit}"
    )
    try:
        return get_histories(user_id, session_id, offset, limit)
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResp(code=400, message="Not found").dict(),
        )


@session_router.patch(
    "/sessions/update_session",
)
async def update_session_partially(update_session_dto: UpdateSessionDTO):
    try:
        title = update_session_dto.title
        order = update_session_dto.order
        user_id = update_session_dto.user_id
        session_id = update_session_dto.session_id
        tab = update_session_dto.tab
        parent_id = update_session_dto.parent_id
        logger.info(
            f"Received request: user_id={user_id}, session_id={session_id}, \
title={title}, order={order}, tab={tab}, parent_id={parent_id}"
        )
        update_session0(user_id, session_id, title, order, tab, parent_id)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResp(code=400, message=e.__str__()).dict(),
        )


@session_router.delete("/sessions/{user_id}/{session_id}")
async def delete_session_by_id(user_id: str, session_id: str):
    logger.info(f"Received request: user_id={user_id}, session_id={session_id}")
    delete_histories(user_id, session_id)


@session_router.post("/sessions/create_session_folder")
async def create_session_folder(folder: NewSessionFolderDTO):
    try:
        user_id = folder.user_id
        title = folder.title
        parent_id = folder.parent_id
        order = folder.order
        logger.info(
            f"Received request: user_id={user_id}, title={title}, \
parent_id={parent_id}, order={order}"
        )
        create_session_folder0(user_id, title, parent_id, order)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResp(code=400, message=e.__str__()).dict(),
        )
