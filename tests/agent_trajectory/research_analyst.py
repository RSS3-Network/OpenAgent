import pytest
from langchain_core.messages import HumanMessage
from loguru import logger

from openagent.agents.research_analyst import build_research_analyst_agent
from openagent.conf.llm_provider import get_available_providers


@pytest.fixture(scope="module")
def research_analyst_agent(request):
    model = request.config.getoption("--model")
    logger.info(f"using model: {model}")

    llm = get_available_providers()[model]
    agent = build_research_analyst_agent(llm)
    return agent


@pytest.mark.asyncio
async def test_query_project(research_analyst_agent):
    events = research_analyst_agent.astream_events(
        {"messages": [HumanMessage(content="Do you know anything about RSS3?", name="human")]}, version="v1"
    )

    tool_end_count = 0

    async for event in events:
        if event["event"] == "on_tool_end":
            event_data_input_ = event["data"]["input"]
            assert event["name"] == "ProjectExecutor"
            assert event_data_input_["keyword"] == "RSS3"
            tool_end_count += 1

    assert tool_end_count > 0, "The on_tool_end event did not occur"


if __name__ == "__main__":
    pytest.main()
