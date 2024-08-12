import pytest
from langchain_core.messages import HumanMessage

from openagent.agents.asset_management import asset_management_agent
from openagent.conf.llm_provider import set_current_llm


@pytest.fixture(autouse=True)
def setup_llm():
    # set_current_llm("gemini-1.5-pro")
    # set_current_llm("gemini-1.5-flash")
    set_current_llm("gpt-3.5-turbo")
    # set_current_llm("llama3.1:latest")

@pytest.mark.asyncio
async def test_swap_eth_to_usdt():
    events = asset_management_agent.astream_events(
        {"messages": [HumanMessage(content="Can you swap 20 eth to usdt ?", name="human")]}, version="v1"
    )

    on_tool_end_count = 0

    async for event in events:
        if event["event"] == "on_tool_end":
            on_tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "SwapExecutor"
            assert event_data_input_["from_token"] == "ETH"
            assert event_data_input_["to_token"] == "USDT"
            assert event_data_input_["amount"] == "20"

    assert on_tool_end_count > 0, "The on_tool_end event did not occur in test_swap_eth_to_usdt"


@pytest.mark.asyncio
async def test_query_user_token_balance():
    events = asset_management_agent.astream_events(
        {"messages": [HumanMessage(content="Can you check 0x33c0814654fa367ce67d8531026eb4481290e63c eth balance ?",
                                   name="human")]},
        version="v1",
    )

    on_tool_end_count = 0

    async for event in events:
        if event["event"] == "on_tool_end":
            on_tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "TokenBalanceExecutor"
            assert event_data_input_["wallet_address"] == "0x33c0814654fa367ce67d8531026eb4481290e63c"
            assert event_data_input_["chain"] == "eth-mainnet"

    assert on_tool_end_count > 0, "The on_tool_end event did not occur in test_query_user_token_balance"


@pytest.mark.asyncio
async def test_query_user_nft_holdings():
    events = asset_management_agent.astream_events(
        {"messages": [HumanMessage(content="Can you check 0x33c0814654fa367ce67d8531026eb4481290e63c nft holdings ?",
                                   name="human")]},
        version="v1",
    )

    on_tool_end_count = 0

    async for event in events:
        if event["event"] == "on_tool_end":
            on_tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "NFTBalanceExecutor"
            assert event_data_input_["wallet_address"] == "0x33c0814654fa367ce67d8531026eb4481290e63c"
            assert event_data_input_["chain"] == "eth-mainnet"

    assert on_tool_end_count > 0, "The on_tool_end event did not occur in test_query_user_nft_holdings"


@pytest.mark.asyncio
async def test_transfer_eth():
    events = asset_management_agent.astream_events(
        {"messages": [HumanMessage(content="Can you transfer 0.5 ETH to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e?",
                                   name="human")]},
        version="v1",
    )

    on_tool_end_count = 0

    async for event in events:
        if event["event"] == "on_tool_end":
            on_tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "TransferExecutor"
            assert event_data_input_["to_address"] == "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
            assert event_data_input_["token"] == "ETH"
            assert event_data_input_["amount"] == "0.5"

    assert on_tool_end_count > 0, "The on_tool_end event did not occur in test_transfer_eth"
