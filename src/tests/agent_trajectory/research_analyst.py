import asyncio
import unittest

from langchain_core.messages import HumanMessage

from openagent.agents.project_management import research_analyst_agent
from openagent.conf.llm_provider import set_current_llm


class TestResearchAnalystAgent(unittest.TestCase):
    def setUp(self):
        # set_current_llm("gemini-1.5-pro")
        set_current_llm("gpt-3.5-turbo")
        # set_current_llm("llama3.1:latest")

    def test_query_project(self):
        async def async_test():
            events = research_analyst_agent.astream_events({"messages": [
                HumanMessage(content="Do you know anything about RSS3?",
                             name="human")]},
                version="v1")

            async for event in events:
                if event['event'] == 'on_tool_end':
                    event_data_input_ = event['data']['input']
                    self.assertEqual(event['name'], 'ProjectExecutor')
                    self.assertEqual(event_data_input_['keyword'], 'RSS3')

        asyncio.run(async_test())


if __name__ == '__main__':
    unittest.main()
