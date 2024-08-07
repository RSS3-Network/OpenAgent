import asyncio
import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain_core.messages import HumanMessage

from openagent.agents.market_analysis import market_analysis_agent
from openagent.conf.llm_provider import set_current_llm
from tests.base_test import BaseAgentTest


class TestMarketAnalysisAgent(BaseAgentTest):
    # def setUp(self):
    #     # set_current_llm("gemini-1.5-pro")
    #     set_current_llm("gpt-3.5-turbo")
    #     # set_current_llm("llama3.1:latest")
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if len(sys.argv) > 2 and not sys.argv[2].startswith('-'):
            set_current_llm(sys.argv[2])
            del sys.argv[2]
        else:
            set_current_llm("default_model")
    def test_query_btc_price(self):
        async def async_test():
            events = market_analysis_agent.astream_events({"messages": [HumanMessage(content="What's BTC price now?", name="human")]}, version="v1")

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "PriceExecutor")
                    self.assertEqual(event_data_input_["token"], "BTC")

        asyncio.run(async_test())

    def test_query_eth_price(self):
        async def async_test():
            events = market_analysis_agent.astream_events(
                {"messages": [HumanMessage(content="What's the current price of Ethereum?", name="human")]}, version="v1"
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "PriceExecutor")
                    self.assertEqual(event_data_input_["token"], "ETH")

        asyncio.run(async_test())

    def test_query_funding_rate(self):
        async def async_test():
            events = market_analysis_agent.astream_events(
                {"messages": [HumanMessage(content="What's the funding rate for BTC/USDT in binance?", name="human")]}, version="v1"
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "FundingRateExecutor")
                    self.assertEqual(event_data_input_["exchange"], "binance")
                    self.assertEqual(event_data_input_["symbol"], "BTC/USDT")

        asyncio.run(async_test())

    def test_query_nft_ranking(self):
        async def async_test():
            events = market_analysis_agent.astream_events(
                {"messages": [HumanMessage(content="What are the top 5 NFT collections?", name="human")]}, version="v1"
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    self.assertEqual(event["name"], "NFTRankingExecutor")

        asyncio.run(async_test())

    def test_query_coin_market(self):
        async def async_test():
            events = market_analysis_agent.astream_events(
                {"messages": [HumanMessage(content="Give me the market cap for Bitcoin", name="human")]}, version="v1"
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "CoinMarketExecutor")
                    self.assertEqual(event_data_input_["order"], "market_cap_desc")

        asyncio.run(async_test())


if __name__ == "__main__":
    unittest.main()
