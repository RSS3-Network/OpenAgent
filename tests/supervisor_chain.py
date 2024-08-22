import pytest
from langchain_core.messages import HumanMessage
from loguru import logger

from openagent.conf.llm_provider import get_available_providers
from openagent.workflows.supervisor_chain import build_supervisor_chain


def next_role(supervisor_chain, query) -> str:
    resp = supervisor_chain.invoke({"messages": [HumanMessage(content=query, name="human")]})
    logger.info(f"response: {resp}")
    return resp["next"]


@pytest.fixture(scope="module")
def supervisor_chain(request):
    model = request.config.getoption("--model")
    logger.info(f"using model: {model}")
    llm = get_available_providers()[model]
    return build_supervisor_chain(llm)


@pytest.mark.parametrize(
    "query,expected_role",
    [
        ("What's the current price of Ethereum and its market trend?", "market_analysis_agent"),
        ("Can you check my ETH balance and show me how to swap some for USDC?", "asset_management_agent"),
        ("swap 1 eth to usdt on ethereum.", "asset_management_agent"),
        ("Can you help me transfer 0.5 ETH to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e on the Ethereum network?", "asset_management_agent"),
        ("What's the latest block height on the Ethereum network, and what are the current gas fees?", "block_explorer_agent"),
        (
            "Can you provide a detailed analysis of the Uniswap project, including its recent developments and market position?",
            "research_analyst_agent",
        ),
        ("What's the weather like today in New York?", "fallback_agent"),
        ("What are the recent DeFi activities for the address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e?", "feed_explorer_agent"),
        ("Show me the latest social interactions for vitalik.eth on Farcaster.", "feed_explorer_agent"),
        ("What are the most recent activities of vitalik.eth from the Uniswap on Ethereum?", "feed_explorer_agent"),
    ],
)
def test_next_role(supervisor_chain, query, expected_role):
    result = next_role(supervisor_chain, query)
    assert result == expected_role, f"Expected {expected_role}, but got {result} for query: {query}"


if __name__ == "__main__":
    pytest.main()
