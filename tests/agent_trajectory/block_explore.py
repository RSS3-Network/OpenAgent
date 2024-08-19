import pytest
from langchain_core.messages import HumanMessage
from loguru import logger

from openagent.agents.block_explore import build_block_explorer_agent
from openagent.conf.llm_provider import get_available_providers


@pytest.fixture(scope="module")
def block_explorer_agent(request):
    model = request.config.getoption("--model")
    logger.info(f"using model: {model}")

    llm = get_available_providers()[model]
    agent = build_block_explorer_agent(llm)
    return agent


@pytest.mark.asyncio
async def test_query_block_height(block_explorer_agent):
    events = block_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="What's the latest block height on the Ethereum network?", name="human")]}, version="v1"
    )

    tool_end_count = 0
    async for event in events:
        if event["event"] == "on_tool_end":
            tool_end_count += 1
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "BlockChainStatExecutor"
            assert event_data_input_["chain"] == "ethereum"

    assert tool_end_count > 0, "The on_tool_end event did not occur"


if __name__ == "__main__":
    pytest.main()
