import asyncio
import unittest

from langchain_core.messages import HumanMessage

from openagent.agents.block_explore import block_explorer_agent
from openagent.conf.llm_provider import set_current_llm


class TestBlockExploreAgent(unittest.TestCase):
    def setUp(self):
        # set_current_llm("gemini-1.5-pro")
        set_current_llm("gpt-3.5-turbo")
        # set_current_llm("llama3.1:latest")

    def test_query_block_height(self):
        async def async_test():
            events = block_explorer_agent.astream_events({"messages": [
                HumanMessage(content="What's the latest block height on the Ethereum network?", name="human")]},
                version="v1")

            async for event in events:
                if event['event'] == 'on_tool_end':
                    event_data_input_ = event['data']['input']
                    self.assertEqual(event['name'], 'BlockChainStatExecutor')
                    self.assertEqual(event_data_input_['chain'], 'ethereum')

        asyncio.run(async_test())


if __name__ == '__main__':
    unittest.main()
