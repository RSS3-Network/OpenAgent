from typing import Optional, Type

from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.dto.mutation import Transfer
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
    description = """Use this tool to transfer cryptocurrencies. for example: \
"transfer 1 ETH to 0x1234567890abcdef1234567890abcdef12345678", \
"transfer 1 BTC to vitalk.eth" and etc. \
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

        return await fetch_transfer(to_address, token, amount)


async def fetch_transfer(to_address: str, token: str, amount: str):
    if not to_address.startswith("0x") and not to_address.endswith(".eth"):
        to_address += ".eth"
    res = {"to_address": to_address, "token": token, "amount": amount}
    token_info = await select_best_token(token)

    transfer = Transfer(
        to_address=res.get("to_address", "1"),
        token=get_token_data_by_key(token_info, "symbol"),
        token_address=get_token_data_by_key(token_info, "address"),
        amount=res.get("amount", "1"),
        logoURI=get_token_data_by_key(token_info, "logoURI"),
        decimals=get_token_data_by_key(token_info, "decimals"),
    )

    return transfer
