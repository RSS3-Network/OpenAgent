import pytest
from langchain_core.messages import HumanMessage
from loguru import logger

from openagent.agents.market_analysis import build_market_analysis_agent
from openagent.conf.llm_provider import get_available_providers


@pytest.fixture(scope="module")
def market_analysis_agent(request):
    model = request.config.getoption("--model")
    logger.info(f"using model: {model}")

    llm = get_available_providers()[model]
    agent = build_market_analysis_agent(llm)
    return agent


@pytest.mark.asyncio
async def test_query_btc_price(market_analysis_agent):
    events = market_analysis_agent.astream_events({"messages": [HumanMessage(content="What's BTC price now?", name="human")]}, version="v1")

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "PriceExecutor"
            assert event_data_input_["token"] == "BTC"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_eth_price(market_analysis_agent):
    events = market_analysis_agent.astream_events(
        {"messages": [HumanMessage(content="What's the current price of Ethereum?", name="human")]}, version="v1"
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "PriceExecutor"
            assert event_data_input_["token"] == "ETH"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_funding_rate(market_analysis_agent):
    events = market_analysis_agent.astream_events(
        {"messages": [HumanMessage(content="What's the funding rate for BTC in binance?", name="human")]}, version="v1"
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "FundingRateExecutor"
            assert event_data_input_["exchange"] == "binance"
            assert event_data_input_["symbol"] == "BTC/USDT"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_nft_ranking(market_analysis_agent):
    events = market_analysis_agent.astream_events(
        {"messages": [HumanMessage(content="What are the top 5 NFT collections?", name="human")]}, version="v1"
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            assert event["name"] == "NFTRankingExecutor"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_coin_market(market_analysis_agent):
    events = market_analysis_agent.astream_events(
        {"messages": [HumanMessage(content="Give me the market cap for Bitcoin", name="human")]}, version="v1"
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "CoinMarketExecutor"
            assert event_data_input_["order"] == "market_cap_desc"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


if __name__ == "__main__":
    pytest.main()
