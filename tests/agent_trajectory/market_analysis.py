import pytest
from langchain_core.messages import HumanMessage

from openagent.agents.market_analysis import market_analysis_agent
from openagent.conf.llm_provider import set_current_llm


@pytest.fixture(scope="module", autouse=True)
def setup_llm():
    # set_current_llm("gemini-1.5-pro")
    # set_current_llm("gemini-1.5-flash")
    set_current_llm("gpt-3.5-turbo")
    # set_current_llm("llama3.1:latest")


@pytest.mark.asyncio
async def test_query_btc_price():
    events = market_analysis_agent.astream_events(
        {"messages": [HumanMessage(content="What's BTC price now?", name="human")]}, version="v1")

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "PriceExecutor"
            assert event_data_input_["token"] == "BTC"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


@pytest.mark.asyncio
async def test_query_eth_price():
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
async def test_query_funding_rate():
    events = market_analysis_agent.astream_events(
        {"messages": [HumanMessage(content="What's the funding rate for BTC/USDT in binance?", name="human")]},
        version="v1"
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
async def test_query_nft_ranking():
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
async def test_query_coin_market():
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
