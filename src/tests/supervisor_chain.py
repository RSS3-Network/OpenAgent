import unittest

from langchain_core.messages import HumanMessage
from loguru import logger

from openagent.conf.llm_provider import set_current_llm
from openagent.workflows.supervisor_chain import build_supervisor_chain


def next_role(query) -> str:
    supervisor_chain = build_supervisor_chain()
    resp = supervisor_chain.invoke({"messages": [HumanMessage(content=query, name="human")]})
    logger.info(f"response: {resp}")
    return resp["next"]


class TestNextRole(unittest.TestCase):
    def setUp(self):
        # set_current_llm("gemini-1.5-pro")
        set_current_llm("gemini-1.5-flash")
        # set_current_llm("gpt-3.5-turbo")
        # set_current_llm("llama3.1:latest")

    def test_market_analysis(self):
        query = "What's the current price of Ethereum and its market trend?"
        expected_role = "market_analysis_agent"
        result = next_role(query)
        self.assertEqual(result, expected_role, f"Expected {expected_role}, but got {result} for query: {query}")

    def test_asset_management(self):
        query = "Can you check my ETH balance and show me how to swap some for USDC?"
        expected_role = "asset_management_agent"
        result = next_role(query)
        self.assertEqual(result, expected_role, f"Expected {expected_role}, but got {result} for query: {query}")

    def test_block_explorer(self):
        query = "What's the latest block height on the Ethereum network, and what are the current gas fees?"
        expected_role = "block_explorer_agent"
        result = next_role(query)
        self.assertEqual(result, expected_role, f"Expected {expected_role}, but got {result} for query: {query}")

    def test_research_analyst(self):
        query = "Can you provide a detailed analysis of the Uniswap project," " including its recent developments and market position?"
        expected_role = "research_analyst_agent"
        result = next_role(query)
        self.assertEqual(result, expected_role, f"Expected {expected_role}, but got {result} for query: {query}")

    def test_fallback(self):
        query = "What's the weather like today in New York?"
        expected_role = "fallback_agent"
        result = next_role(query)
        self.assertEqual(result, expected_role, f"Expected {expected_role}, but got {result} for query: {query}")

    def test_multi_step_query(self):
        query = (
            "I want to invest in a promising DeFi project. Can you first give me an "
            "overview of the current DeFi market trends, then recommend a project, "
            "and finally show me how to acquire some tokens of that project?"
        )
        expected_role = "market_analysis_agent"
        result = next_role(query)
        self.assertEqual(result, expected_role, f"Expected {expected_role}, but got {result} for query: {query}")

    def test_feed_explorer(self):
        query = "What are the recent DeFi activities for the address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e?"
        expected_role = "feed_explorer_agent"
        result = next_role(query)
        self.assertEqual(result, expected_role, f"Expected {expected_role}, but got {result} for query: {query}")

    def test_feed_explorer_social(self):
        query = "Show me the latest social interactions for vitalik.eth on Farcaster."
        expected_role = "feed_explorer_agent"
        result = next_role(query)
        self.assertEqual(result, expected_role, f"Expected {expected_role}, but got {result} for query: {query}")

    def test_feed_explorer_source(self):
        query = "What are the most recent activities of vitalik.eth from the Uniswap on Ethereum?"
        expected_role = "feed_explorer_agent"
        result = next_role(query)
        self.assertEqual(result, expected_role, f"Expected {expected_role}, but got {result} for query: {query}")

if __name__ == "__main__":
    unittest.main()
