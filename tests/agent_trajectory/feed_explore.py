import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from langchain_core.messages import HumanMessage

from openagent.agents.feed_explore import feed_explorer_agent
from openagent.conf.llm_provider import set_current_llm
from tests.base_test import BaseAgentTest


class TestFeedExploreAgent(BaseAgentTest):
    # def setUp(self):
    #     set_current_llm("gpt-3.5-turbo")
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if len(sys.argv) > 2 and not sys.argv[2].startswith("-"):
            set_current_llm(sys.argv[2])
            del sys.argv[2]
        else:
            set_current_llm("default_model")

    def test_query_defi_activities(self):
        """
        Test querying recent DeFi activities for a specific Ethereum address.
        Validates that the response contains the correct address and is handled by the 'DeFiExecutor'.
        """

        async def async_test():
            events = feed_explorer_agent.astream_events(
                {
                    "messages": [
                        HumanMessage(content="Show me recent DeFi activities for address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e", name="human")
                    ]
                },
                version="v1",
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "DeFiExecutor")
                    self.assertEqual(event_data_input_["address"], "0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
                    self.assertEqual(event_data_input_["activity_type"], "all")

        asyncio.run(async_test())

    def test_query_social_activities(self):
        """
        Test querying recent social activities for a specific ENS name (vitalik.eth).
        Validates that the response contains the correct address and is handled by the 'FeedExecutor'.
        """

        async def async_test():
            events = feed_explorer_agent.astream_events(
                {"messages": [HumanMessage(content="What are the recent activities for vitalik.eth?", name="human")]}, version="v1"
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "FeedExecutor")
                    self.assertIn("address", event_data_input_)
                    self.assertEqual(event_data_input_["address"], "vitalik.eth")

        asyncio.run(async_test())

    def test_query_feed_source(self):
        """
        Test querying the latest activities for a specific ENS name (vitalik.eth) from a specific platform (Uniswap) on a specific network (Ethereum).
        Validates that the response contains the correct platform, network, and address and is handled by the 'FeedSourceExecutor'.
        """

        async def async_test():
            events = feed_explorer_agent.astream_events(
                {"messages": [HumanMessage(content="Show me the latest activities of vitalik.eth from Uniswap on Ethereum", name="human")]},
                version="v1",
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "FeedSourceExecutor")
                    self.assertIn("platform", event_data_input_)
                    self.assertEqual(event_data_input_["platform"], "Uniswap")
                    self.assertIn("network", event_data_input_)
                    self.assertEqual(event_data_input_["network"], "ethereum")
                    self.assertIn("address", event_data_input_)
                    self.assertEqual(event_data_input_["address"], "vitalik.eth")

        asyncio.run(async_test())

    def test_query_unsupported_network(self):
        """
        Test querying activities on an unsupported network (XYZ).
        Validates that the response indicates the network is unsupported and mentions the network name (XYZ).
        """

        async def async_test():
            events = feed_explorer_agent.astream_events(
                {"messages": [HumanMessage(content="Show me activities on the XYZ network", name="human")]}, version="v1"
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    self.assertIn("output", event["data"])
                    self.assertIn("Unsupported network", event["data"]["output"])
                    self.assertIn("XYZ", event["data"]["output"])

        asyncio.run(async_test())

    def test_query_multiple_addresses(self):
        """
        Test querying and comparing activities for multiple addresses (vitalik.eth and a specific Ethereum address).
        Validates that the response contains both addresses.
        """

        async def async_test():
            events = feed_explorer_agent.astream_events(
                {
                    "messages": [
                        HumanMessage(content="Compare activities of vitalik.eth and 0x742d35Cc6634C0532925a3b844Bc454e4438f44e", name="human")
                    ]
                },
                version="v1",
            )

            addresses_checked = set()
            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertIn("address", event_data_input_)
                    addresses_checked.add(event_data_input_["address"])

            self.assertEqual(len(addresses_checked), 2)
            self.assertIn("vitalik.eth", addresses_checked)
            self.assertIn("0x742d35Cc6634C0532925a3b844Bc454e4438f44e", addresses_checked)

        asyncio.run(async_test())


if __name__ == "__main__":
    unittest.main()
