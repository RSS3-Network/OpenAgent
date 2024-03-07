import asyncio
import uuid
from typing import AsyncIterable


from langchain.callbacks import LLMonitorCallbackHandler
from sqlalchemy.exc import NoResultFound

from openagent.agent.ctx_var import resp_msg_id, chat_req_ctx
from openagent.agent.function_agent import get_agent
from openagent.agent.suggested_question import agen_suggested_questions
from openagent.agent.session_title import agen_session_title
from openagent.agent.stream_callback import StreamCallbackHandler
from openagent.db.database import DBSession
from openagent.db.models import ChatSession, ChatHistory
from openagent.dto.cb_content import CbContentType, CbContent
from openagent.dto.chat_req import ChatReq
from openagent.dto.chat_resp import ChatResp, ChatRespType


async def arun_agent(
    req: ChatReq, stream_cb: StreamCallbackHandler, resp_msg_id0, monitoring_cb
):
    agent = get_agent(req.session_id)
    resp_msg_id.set(resp_msg_id0)
    chat_req_ctx.set(req)
    return await agent.arun(
        req.body,
        callbacks=[stream_cb, monitoring_cb],
        metadata={
            "agentName": "openagent-backend",
            "userId": req.user_id,
        },
    )


async def answer(req: ChatReq) -> AsyncIterable[str]:
    try:
        create_session = await need_create_session(req)
    except Exception as e:
        yield ChatResp(
            type=ChatRespType.error, message_id=None, body=e.__str__()
        ).model_dump_json()
        return

    stream_cb = StreamCallbackHandler()
    monitoring_cb = LLMonitorCallbackHandler()

    resp_msg_id0 = str(uuid.uuid4())

    chat_task = asyncio.create_task(
        arun_agent(req, stream_cb, resp_msg_id0, monitoring_cb)
    )

    suggested_questions_task = asyncio.create_task(
        agen_suggested_questions(req.user_id, req.body, monitoring_cb)
    )

    session_title_task = None
    if create_session:
        session_title_task = asyncio.create_task(
            agen_session_title(req.user_id, req.session_id, req.body, monitoring_cb)
        )

    try:
        is_suggested_questions_done = False
        is_session_title_done = False
        async for cb_content in stream_cb.aiter():
            yield await gen_agent_resp(cb_content, resp_msg_id0)

            if suggested_questions_task.done() and not is_suggested_questions_done:
                is_suggested_questions_done = True
                yield await gen_suggested_questions(
                    suggested_questions_task, resp_msg_id0
                )

            if (
                create_session
                and session_title_task.done()  # type: ignore
                and not is_session_title_done
            ):
                is_session_title_done = True
                yield await gen_session_title(resp_msg_id0, session_title_task)

        if not is_suggested_questions_done:
            yield await gen_suggested_questions(suggested_questions_task, resp_msg_id0)

        if create_session and not is_session_title_done:
            yield await gen_session_title(resp_msg_id0, session_title_task)

    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        stream_cb.done.set()
    await chat_task


async def gen_agent_resp(cb_content: CbContent, resp_msg_id0):
    resp_type = get_resp_type(cb_content.type)
    resp = ChatResp(
        message_id=resp_msg_id0,
        block_id=cb_content.block_id,
        type=resp_type,
        body=cb_content.content,
    )
    return resp.model_dump_json()


async def gen_session_title(resp_msg_id0, session_title_task):
    session_title = await session_title_task
    return ChatResp(
        message_id=resp_msg_id0,
        type=ChatRespType.session_title,
        body=session_title,
    ).model_dump_json()


async def gen_suggested_questions(suggested_questions_task, resp_msg_id0):
    questions = await suggested_questions_task
    return ChatResp(
        message_id=resp_msg_id0,
        type=ChatRespType.suggested_questions,
        body=questions,
    ).model_dump_json()


def get_resp_type(cb_content_type: CbContentType) -> ChatRespType:
    if cb_content_type == CbContentType.llm_content:
        return ChatRespType.natural_language
    if cb_content_type == CbContentType.tool_content:
        return ChatRespType.tool
    raise ValueError(f"Unknown cb_content_type: {cb_content_type}")


async def need_create_session(req):
    session_id = req.session_id
    with DBSession() as db_session:
        try:
            session = (
                db_session.query(ChatSession)
                .filter(ChatSession.session_id == session_id)
                .one()
            )
            if session.deleted_at is not None:
                raise ValueError("Session is deleted")
            if (
                db_session.query(ChatHistory)
                .filter(ChatHistory.message_id == req.message_id)
                .count()
                > 0
            ):
                raise ValueError("Message id already exists")
        except NoResultFound:
            db_session.add(
                ChatSession(
                    session_id=session_id,
                    user_id=req.user_id,
                )
            )
            db_session.commit()
            return True
        return False
