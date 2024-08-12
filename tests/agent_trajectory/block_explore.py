import pytest
from langchain_core.messages import HumanMessage

from openagent.agents.block_explore import block_explorer_agent
from openagent.conf.llm_provider import set_current_llm


@pytest.fixture(scope="module", autouse=True)
def setup_llm():
    # set_current_llm("gemini-1.5-pro")
    # set_current_llm("gemini-1.5-flash")
    set_current_llm("gpt-3.5-turbo")
    # set_current_llm("llama3.1:latest")


@pytest.mark.asyncio
async def test_query_block_height():
    events = block_explorer_agent.astream_events(
        {"messages": [HumanMessage(content="What's the latest block height on the Ethereum network?", name="human")]},
        version="v1"
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
