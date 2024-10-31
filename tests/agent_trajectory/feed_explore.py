import pytest
from langchain_core.messages import HumanMessage
from loguru import logger

from openagent.agents.feed_explore import build_feed_explorer_agent
from openagent.conf.llm_provider import get_available_providers


@pytest.fixture(scope="module")
def feed_explorer_agent(request):
    model = request.config.getoption("--model")
    logger.info(f"using model: {model}")
    llm = get_available_providers()[model]
    agent = build_feed_explorer_agent(llm)
    return agent


@pytest.mark.asyncio
async def test_query_defi_activities(feed_explorer_agent):
    events = feed_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="Show me recent DeFi activities for address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e", name="human")]},
        version="v1",
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "DeFiExecutor"
            assert event_data_input_["address"] == "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
            assert event_data_input_["activity_type"] == "all"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_social_activities(feed_explorer_agent):
    events = feed_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="What are the recent activities for vitalik.eth?", name="human")]}, version="v1"
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "FeedExecutor"
            assert "address" in event_data_input_
            assert event_data_input_["address"] == "vitalik.eth"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_feed_source(feed_explorer_agent):
    events = feed_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="Show me the latest activities of vitalik.eth from Uniswap on Ethereum", name="human")]},
        version="v1",
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "FeedSourceExecutor"
            assert "platform" in event_data_input_
            assert event_data_input_["platform"] == "Uniswap"
            assert "network" in event_data_input_
            assert event_data_input_["network"] == "ethereum"
            assert "address" in event_data_input_
            assert event_data_input_["address"] == "vitalik.eth"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_unsupported_network(feed_explorer_agent):
    events = feed_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="Show me activities on the XYZ network", name="human")]}, version="v1"
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            assert "output" in event["data"]
            assert "Unsupported network" in event["data"]["output"]

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_multiple_addresses(feed_explorer_agent):
    events = feed_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="Compare activities of vitalik.eth and 0x742d35Cc6634C0532925a3b844Bc454e4438f44e", name="human")]},
        version="v1",
    )

    addresses_checked = set()
    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert "address" in event_data_input_
            addresses_checked.add(event_data_input_["address"])

    assert tool_end_count > 0, "The on_tool_end event did not occur"
    assert len(addresses_checked) == 2
    assert "vitalik.eth" in addresses_checked
    assert "0x742d35Cc6634C0532925a3b844Bc454e4438f44e" in addresses_checked


if __name__ == "__main__":
    pytest.main()
