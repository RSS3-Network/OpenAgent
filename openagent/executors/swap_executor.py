import asyncio
from typing import Literal, Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from openagent.executors.token_util import chain_name_to_id, get_token_data_by_key, select_best_token


class Swap(BaseModel):
    from_token: str
    from_token_address: str
    to_token: str
    to_token_address: str
    amount: str
    type: str = "swap"
    from_chain_name: str
    to_chain_name: str


ChainLiteral = Literal["ETH", "BSC", "ARBITRUM", "OPTIMISM", "POLYGON"]


class ParamSchema(BaseModel):
    """
    Schema for the parameters required for a token swap.
    """

    from_token: str = Field(description="Symbol of the token to swap from, e.g., 'BTC', 'ETH', 'RSS3', 'USDT', 'USDC'. Default: 'ETH'.")
    to_token: str = Field(description="Symbol of the token to swap to, e.g., 'BTC', 'ETH', 'RSS3', 'USDT', 'USDC'. Default: 'ETH'.")
    from_chain: ChainLiteral = Field(
        default="ETH",
        description="Blockchain network to swap from, support networks: 'ETH', 'BSC', 'ARBITRUM', 'OPTIMISM', 'POLYGON'. Default: 'ETH'.",
    )
    to_chain: ChainLiteral = Field(
        default="ETH",
        description="Blockchain network to swap to, support networks: 'ETH', 'BSC', 'ARBITRUM', 'OPTIMISM', 'POLYGON'. Default: 'ETH'.",
    )
    amount: str = Field(description="Amount of the from-side token to swap, e.g., '0.1', '1', '10'. Default: '1'.")


class SwapExecutor(BaseTool):
    """
    Tool for generating a swap widget for cryptocurrency swaps.
    """

    name = "SwapExecutor"
    description = "Use this tool to handle user requests to swap cryptocurrencies."
    args_schema: Type[ParamSchema] = ParamSchema
    return_direct = False

    def _run(
        self,
        from_token: str,
        to_token: str,
        from_chain: ChainLiteral,
        to_chain: ChainLiteral,
        amount: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

    async def _arun(
        self,
        from_token: str,
        to_token: str,
        from_chain: ChainLiteral = "ETH",
        to_chain: ChainLiteral = "ETH",
        amount: str = "1",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        return await fetch_swap(from_token, to_token, from_chain, to_chain, amount)


async def fetch_swap(from_token: str, to_token: str, from_chain: ChainLiteral, to_chain: ChainLiteral, amount: str):
    """
    Fetch the swap details for the given parameters.

    Args:
        from_token (str): The symbol of the from-side token.
        to_token (str): The symbol of the to-side token.
        from_chain (ChainLiteral): The from-side blockchain network.
        to_chain (ChainLiteral): The to-side blockchain network.
        amount (str): The amount of tokens to swap.

    Returns:
        str: The swap details in JSON format.
    """
    from_chain_id = chain_name_to_id(from_chain)
    to_chain_id = chain_name_to_id(to_chain)

    # Fetch token data concurrently
    from_token_data, to_token_data = await asyncio.gather(select_best_token(from_token, from_chain_id), select_best_token(to_token, to_chain_id))

    swap = Swap(
        from_token=get_token_data_by_key(from_token_data, "symbol"),
        from_token_address=get_token_data_by_key(from_token_data, "address"),
        to_token=get_token_data_by_key(to_token_data, "symbol"),
        to_token_address=get_token_data_by_key(to_token_data, "address"),
        from_chain_name=from_chain,
        to_chain_name=to_chain,
        amount=amount,
    )
    return swap.model_dump_json()
