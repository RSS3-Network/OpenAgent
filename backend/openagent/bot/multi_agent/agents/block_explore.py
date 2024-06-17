from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.bot.multi_agent.agents.agent_factory import create_agent
from openagent.bot.multi_agent.tools.tavily_tool import tavily_tool
from openagent.experts.block_stat_expert import BlockStatExpert

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

block_explorer_agent = create_agent(
    llm,
    [BlockStatExpert(), tavily_tool],
    """
    You are BlockExplorer, dedicated to exploring and presenting detailed blockchain information.
    Help users query transaction details, block data, gas fees, block height, and other blockchain-related information.
    Use the available tools to gather and display accurate blockchain data.
""",
)
