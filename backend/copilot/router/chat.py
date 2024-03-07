from fastapi import APIRouter
from loguru import logger
from sse_starlette import EventSourceResponse

from copilot.dto.chat_req import ChatReq
from copilot.dto.chat_resp import ChatResp
from copilot.service.chat import answer

chat_router = APIRouter(tags=["Chat"])


@chat_router.post("/stream_chat/", response_model=ChatResp)
async def stream_chat(req: ChatReq):
    logger.info(f"Received request: req={req}")
    generator = answer(req)
    return EventSourceResponse(generator)
