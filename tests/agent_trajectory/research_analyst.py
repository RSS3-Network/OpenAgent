import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from langchain_core.messages import HumanMessage

from openagent.agents.project_management import research_analyst_agent
from openagent.conf.llm_provider import set_current_llm
from tests.base_test import BaseAgentTest


class TestResearchAnalystAgent(BaseAgentTest):
    # def setUp(self):
    #     # set_current_llm("gemini-1.5-pro")
    #     set_current_llm("gpt-3.5-turbo")
    #     # set_current_llm("llama3.1:latest")
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if len(sys.argv) > 2 and not sys.argv[2].startswith("-"):
            set_current_llm(sys.argv[2])
            del sys.argv[2]
        else:
            set_current_llm("default_model")

    def test_query_project(self):
        async def async_test():
            events = research_analyst_agent.astream_events(
                {"messages": [HumanMessage(content="Do you know anything about RSS3?", name="human")]}, version="v1"
            )

            async for event in events:
                if event["event"] == "on_tool_end":
                    event_data_input_ = event["data"]["input"]
                    self.assertEqual(event["name"], "ProjectExecutor")
                    self.assertEqual(event_data_input_["keyword"], "RSS3")

        asyncio.run(async_test())


if __name__ == "__main__":
    unittest.main()
