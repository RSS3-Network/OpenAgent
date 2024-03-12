import uuid
from datetime import datetime
from typing import Optional, Type


from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.agent.ctx_var import chat_req_ctx
from openagent.db.database import DBSession
from openagent.db.models import Task
from openagent.dto.mutation import Transfer
from openagent.dto.task import TaskStatus, TaskType, TransferDTO, ConfirmTransferDTO
from openagent.router.task import confirm_transfer
from openagent.experts import (
    get_token_data_by_key,
    select_best_token,
)


class ParamSchema(BaseModel):
    to_address: str = Field(
        description="""extract the address mentioned in the query,
like : "0x1234567890abcdef1234567890abcdef12345678", "vitalk.eth" and etc.
If the address does not start with '0x' and also does not end with '.eth',
a '.eth' ending should be added to it.
"""
    )

    token: str = Field(
        description="""extract the cryptocurrencies mentioned in the query,
like: "BTC", "ETH", "RSS3", "USDT", "USDC" and etc. Default is "ETH"."""
    )

    amount: str = Field(
        description="""extract the amount of cryptocurrencies mentioned in the query,
like: "0.1", "1", "10" and etc. Default is "1"."""
    )

    status: str = Field(
        description="""extract the status of the transaction mentioned in the query,
like: "pending", "editing" or "running". Default is "pending", when user edit the transaction,
 the status will be "editing", when user confirm the transaction, the status will be "running"."""
    )


class TransferExpert(BaseTool):
    name = "transfer"
    description = """Use this tool to extract structured information from the user's query,
whenever the query is about a transfer or sending cryptocurrencies to someone.
A transfer indicates an action of sending an amount of token to an address or a blockchain domain.\n
"""
    args_schema: Type[ParamSchema] = ParamSchema
    return_direct = False
    last_task_id: Optional[str] = None

    def _run(
        self,
        to_address: str,
        token: str,
        amount: str,
        status: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        to_address: str,
        token: str,
        amount: str,
        status: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        if status == "pending" or self.last_task_id is None:
            self.last_task_id = str(uuid.uuid4())

        transfer = await fetch_transfer(to_address, token, amount, self.last_task_id)

        if status == "pending":
            await save_new_task(transfer)

        elif status == "running":
            chat_req = chat_req_ctx.get()
            confirm_transfer_dto = ConfirmTransferDTO(
                user_id=chat_req.user_id,
                task_id=self.last_task_id,
                executor_id=1,
                to_address=transfer.to_address,
                amount=transfer.amount,
                token_address=transfer.token_address,
            )
            return await confirm_transfer(confirm_transfer_dto)

        return transfer.model_dump_json()


async def fetch_transfer(to_address: str, token: str, amount: str, task_id: str):
    if not to_address.startswith("0x") and not to_address.endswith(".eth"):
        to_address += ".eth"
    res = {"to_address": to_address, "token": token, "amount": amount}
    token_info = await select_best_token(token)

    transfer = Transfer(
        task_id=task_id,
        to_address=res.get("to_address", "1"),
        token=get_token_data_by_key(token_info, "symbol"),
        token_address=get_token_data_by_key(token_info, "address"),
        amount=res.get("amount", "1"),
        logoURI=get_token_data_by_key(token_info, "logoURI"),
        decimals=get_token_data_by_key(token_info, "decimals"),
    )

    return transfer


async def save_new_task(transfer):
    with DBSession() as db_session:
        chat_req = chat_req_ctx.get()
        task = Task(
            user_id=chat_req.user_id,
            session_id=chat_req.session_id,
            task_id=transfer.task_id,
            type=TaskType.transfer,
            body=TransferDTO(
                user_id=chat_req.user_id,
                task_id=transfer.task_id,
                executor_id=-1,
                to_address=transfer.to_address,
                amount=transfer.amount,
                token_address=transfer.token_address,
                token=transfer.token,
                logoURI=transfer.logoURI,
                decimals=transfer.decimals,
            ).model_dump_json(),
            status=TaskStatus.idle,
            created_at=datetime.utcnow(),
        )
        db_session.add(task)
        db_session.commit()
