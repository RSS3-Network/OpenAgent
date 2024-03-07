from contextvars import ContextVar

from copilot.dto.chat_req import ChatReq

resp_msg_id: ContextVar[str | None] = ContextVar("resp_msg_id", default=None)
chat_req_ctx: ContextVar[ChatReq] = ContextVar("chat_req_ctx")
