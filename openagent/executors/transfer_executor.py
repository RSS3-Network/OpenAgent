from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.executors.token_util import chain_name_to_id, get_token_data_by_key, select_best_token


class Transfer(BaseModel):
    # task_id: str
    to_address: str
    token: str
    token_address: str
    chain_id: str
    amount: str
    logoURI: str  # noqa
    decimals: int


class ParamSchema(BaseModel):
    """
    Defines the schema for input parameters of the TransferExecutor tool.
    """

    to_address: str = Field(
        description="""extract the blockchain address mentioned in the query""",
    )

    token: str = Field(
        description="""extract the token symbol mentioned in the query""",
    )

    chain_name: str = Field(
        default="ethereum",
        description="""extract the blockchain name mentioned in the query,
if not mentioned, default is "ethereum".""",
    )

    amount: str = Field(
        default="1",
        description="""extract the amount of cryptocurrencies mentioned in the query,
if not mentioned, default is "1".""",
    )


class TransferExecutor(BaseTool):
    """
    Tool for generating a transfer widget for cryptocurrency transfers.
    """

    name = "TransferExecutor"
    description = """Use this tool to send cryptocurrencies to another address."""
    args_schema: Type[ParamSchema] = ParamSchema
    return_direct = False
    last_task_id: Optional[str] = None

    def _run(
        self,
        to_address: str,
        token: str,
        chain_name: str,
        amount: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        to_address: str,
        token: str,
        chain_name: str = "ethereum",
        amount: str = "1",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        """
        Asynchronously run the transfer process.

        :param to_address: The recipient's blockchain address
        :param token: The token symbol
        :param chain_name: The blockchain name (default is "ethereum")
        :param amount: The amount to transfer (default is "1")
        :param run_manager: Optional callback manager for async operations
        :return: JSON representation of the transfer details
        """

        return await fetch_transfer(to_address, token, chain_name, amount)


async def fetch_transfer(to_address: str, token: str, chain_name: str, amount: str):
    """
    Fetch transfer details and prepare the Transfer object.

    :param to_address: The recipient's blockchain address
    :param token: The token symbol
    :param chain_name: The blockchain name
    :param amount: The amount to transfer
    :return: JSON representation of the Transfer object
    """

    if not to_address.startswith("0x") and not to_address.endswith(".eth"):
        to_address += ".eth"
    chain_id = chain_name_to_id(chain_name)
    res = {
        "to_address": to_address,
        "token": token,
        "amount": amount,
    }

    # Select the best token based on the provided token symbol and chain ID
    token_info = await select_best_token(token, chain_id)

    # Create a Transfer object with all the necessary information
    transfer = Transfer(
        to_address=res.get("to_address", "1"),
        token=get_token_data_by_key(token_info, "symbol"),
        token_address=get_token_data_by_key(token_info, "address"),
        chain_id=chain_id,
        amount=res.get("amount", "1"),
        logoURI=get_token_data_by_key(token_info, "logoURI"),
        decimals=get_token_data_by_key(token_info, "decimals"),
    )

    return transfer.model_dump_json()
