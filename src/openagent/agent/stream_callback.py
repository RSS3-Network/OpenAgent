import asyncio
import json
import uuid
from typing import Any, AsyncIterator, Dict, List, Literal, Optional, Union, cast
from uuid import UUID

from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import AgentFinish, BaseMessage, LLMResult, _message_to_dict

from openagent.agent.ctx_var import chat_req_ctx, resp_msg_id
from openagent.db.database import DBSession
from openagent.db.models import ChatHistory
from openagent.dto.cb_content import CbContent, CbContentType


class StreamCallbackHandler(AsyncCallbackHandler):
    queue: asyncio.Queue[CbContent]

    done: asyncio.Event
    is_on_chain_start_called: bool = False

    current_llm_block_id: Optional[str] = None
    current_tool_block_id: Optional[str] = None

    current_tool_start_content: Optional[dict] = None

    @property
    def always_verbose(self) -> bool:
        return True

    def __init__(self) -> None:
        self.queue = asyncio.Queue()
        self.done = asyncio.Event()

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        # If two calls are made in a row, this resets the state
        self.done.clear()
        self.current_llm_block_id = str(uuid.uuid4())

    async def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        output_str = response.generations[0][0].text
        if output_str is None or output_str == "":
            return

        with DBSession() as db_session:
            msg_id = resp_msg_id.get()
            chat_req = chat_req_ctx.get()

            ai_message = BaseMessage(
                content=output_str,
                type="ai",
                additional_kwargs={"block_id": self.current_llm_block_id},
            )
            db_session.add(
                ChatHistory(
                    user_id=chat_req.user_id,
                    message_id=msg_id,
                    session_id=chat_req.session_id,
                    message=json.dumps(_message_to_dict(ai_message)),
                )
            )
            db_session.commit()

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        if token is not None and token != "":
            self.queue.put_nowait(
                CbContent(
                    content=token,
                    type=CbContentType.llm_content,
                    block_id=self.current_llm_block_id,
                )
            )

    async def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        if self.is_on_chain_start_called:
            return

        self.is_on_chain_start_called = True
        with DBSession() as db_session:
            chat_req = chat_req_ctx.get()
            human_message = BaseMessage(
                content=inputs["input"],
                type="human",
                additional_kwargs={"block_id": str(uuid.uuid4())},
            )
            db_session.add(
                ChatHistory(
                    user_id=chat_req.user_id,
                    message_id=chat_req.message_id,
                    session_id=chat_req.session_id,
                    message=json.dumps(_message_to_dict(human_message)),
                )
            )
            db_session.commit()

    def show_tool_block(self, tool_name) -> bool:
        if tool_name in [
            "token",
            "swap",
            "transfer",
            "collection",
            "network",
            "feed",
            "dapp",
            "account",
            "executor",
        ]:
            return True
        return False

    async def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        tool_name = serialized["name"]
        show = self.show_tool_block(tool_name)
        if not show:
            return
        self.current_tool_block_id = str(uuid.uuid4())

        try:
            tool_input = json.loads(input_str.replace("'", '"'))
        except Exception:
            tool_input = ""
        await self.queue.put(
            CbContent(
                content={
                    "tool_name": tool_name,
                    "input": tool_input,
                },
                type=CbContentType.tool_content,
                block_id=self.current_tool_block_id,
            )
        )

        self.current_tool_start_content = tool_input

    async def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        tool_name = kwargs["name"]
        show = self.show_tool_block(tool_name)
        if not show:
            return
        try:
            end_index = output.rfind("}")
            output_str = output[: end_index + 1]
            output_json = json.loads(output_str)
        except Exception:
            output_json = json.loads(output)

        await self.queue.put(
            CbContent(
                content={"tool_name": tool_name, "output": output_json},
                type=CbContentType.tool_content,
                block_id=self.current_tool_block_id,
            )
        )
        with DBSession() as db_session:
            msg_id = resp_msg_id.get()
            chat_req = chat_req_ctx.get()
            ai_message = BaseMessage(
                content=json.dumps(
                    {
                        "tool_name": tool_name,
                        "output": output_json,
                        "input": self.current_tool_start_content,
                    }
                ),
                type="tool",
                additional_kwargs={"block_id": self.current_tool_block_id},
            )
            db_session.add(
                ChatHistory(
                    user_id=chat_req.user_id,
                    message_id=msg_id,
                    session_id=chat_req.session_id,
                    message=json.dumps(_message_to_dict(ai_message)),
                )
            )
            db_session.commit()

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        self.done.set()

    async def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        self.done.set()
        return await super().on_llm_error(
            error, run_id=run_id, parent_run_id=parent_run_id, tags=tags, **kwargs
        )

    # TODO implement the other methods

    async def aiter(self) -> AsyncIterator[CbContent]:
        while not self.queue.empty() or not self.done.is_set():
            # Wait for the next token in the queue,
            # but stop waiting if the done event is set
            done, other = await asyncio.wait(
                [
                    # NOTE: If you add other tasks here, update the code below,
                    # which assumes each set has exactly one task each
                    asyncio.ensure_future(self.queue.get()),
                    asyncio.ensure_future(self.done.wait()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # Cancel the other task
            if other:
                other.pop().cancel()

            # Extract the value of the first completed task
            token_or_done = cast(Union[CbContent, Literal[True]], done.pop().result())

            # If the extracted value is the boolean True, the done event was set
            if token_or_done is True:
                break

            # Otherwise, the extracted value is a token, which we yield
            yield token_or_done
