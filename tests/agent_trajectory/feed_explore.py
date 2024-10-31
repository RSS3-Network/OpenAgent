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
async def test_query_social_activities(feed_explorer_agent):
    events = feed_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="What are the recent activities for vitalik.eth?", name="human")]}, 
        version="v1"
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "FeedExecutor"
            assert "address" in event_data_input_
            assert event_data_input_["address"] == "vitalik.eth"
            assert "type" in event_data_input_
            assert event_data_input_["type"] in ["all", "post", "comment", "share"]

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_specific_activity_type(feed_explorer_agent):
    events = feed_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="Show me recent posts from vitalik.eth", name="human")]},
        version="v1",
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "FeedExecutor"
            assert event_data_input_["address"] == "vitalik.eth"
            assert event_data_input_["type"] == "post"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_telegram_news(feed_explorer_agent):
    events = feed_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="Show me the latest crypto news", name="human")]},
        version="v1",
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            assert event["name"] == "TelegramNewsExecutor"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_limited_news(feed_explorer_agent):
    events = feed_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="Get me the latest 5 news updates from crypto channels", name="human")]},
        version="v1",
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            assert event["name"] == "TelegramNewsExecutor"
            event_data_input_ = event["data"]["input"]
            assert event_data_input_["limit"] == 5

    assert tool_end_count > 0, "The on_tool_end event did not occur"


if __name__ == "__main__":
    pytest.main()
