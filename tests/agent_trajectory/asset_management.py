import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from langchain_core.messages import HumanMessage

from openagent.agents.asset_management import asset_management_agent
from openagent.conf.llm_provider import set_current_llm
from tests.base_test import BaseAgentTest


class TestAssetManagementAgent(BaseAgentTest):
    # def setUp(self):
    #     set_current_llm("gemini-1.5-pro")
    #     # set_current_llm("gpt-3.5-turbo")
    #     # set_current_llm("llama3.1:latest")
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if len(sys.argv) > 2 and not sys.argv[2].startswith("-"):
            set_current_llm(sys.argv[2])
            del sys.argv[2]
        else:
            set_current_llm("default_model")

    def test_swap_eth_to_usdt(self):
        async def async_test():
            events = asset_management_agent.astream_events(
                {"messages": [HumanMessage(content="Can you swap 20 eth to usdt ?", name="human")]}, version="v1"
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "SwapExecutor")
                    self.assertEqual(event_data_input_["from_token"], "ETH")
                    self.assertEqual(event_data_input_["to_token"], "USDT")
                    self.assertEqual(event_data_input_["amount"], "20")

        asyncio.run(async_test())

    def test_query_user_token_balance(self):
        async def async_test():
            events = asset_management_agent.astream_events(
                {"messages": [HumanMessage(content="Can you check 0x33c0814654fa367ce67d8531026eb4481290e63c eth balance ?", name="human")]},
                version="v1",
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "TokenBalanceExecutor")
                    self.assertEqual(event_data_input_["wallet_address"], "0x33c0814654fa367ce67d8531026eb4481290e63c")
                    self.assertEqual(event_data_input_["chain"], "eth-mainnet")

        asyncio.run(async_test())

    def test_query_user_nft_holdings(self):
        async def async_test():
            events = asset_management_agent.astream_events(
                {"messages": [HumanMessage(content="Can you check 0x33c0814654fa367ce67d8531026eb4481290e63c nft holdings ?", name="human")]},
                version="v1",
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "NFTBalanceExecutor")
                    self.assertEqual(event_data_input_["wallet_address"], "0x33c0814654fa367ce67d8531026eb4481290e63c")
                    self.assertEqual(event_data_input_["chain"], "eth-mainnet")

        asyncio.run(async_test())

    def test_transfer_eth(self):
        async def async_test():
            events = asset_management_agent.astream_events(
                {"messages": [HumanMessage(content="Can you transfer 0.5 ETH to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e?", name="human")]},
                version="v1",
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "TransferExecutor")
                    self.assertEqual(event_data_input_["to_address"], "0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
                    self.assertEqual(event_data_input_["token"], "ETH")
                    self.assertEqual(event_data_input_["amount"], "0.5")

        asyncio.run(async_test())


if __name__ == "__main__":
    unittest.main()
