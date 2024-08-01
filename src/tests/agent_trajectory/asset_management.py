import asyncio
import unittest

from langchain_core.messages import HumanMessage

from openagent.agents.asset_management import asset_management_agent
from openagent.conf.llm_provider import set_current_llm


class TestAssetManagementAgent(unittest.TestCase):
    def setUp(self):
        set_current_llm("gemini-1.5-pro")
        # set_current_llm("gpt-3.5-turbo")
        # set_current_llm("llama3.1:latest")

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


if __name__ == "__main__":
    unittest.main()
