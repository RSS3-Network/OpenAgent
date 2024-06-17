from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.bot.multi_agent.agents.agent_factory import create_agent
from openagent.bot.multi_agent.tools.nft_balance_tool import NFTBalanceTool
from openagent.bot.multi_agent.tools.token_balance_tool import TokenBalanceTool

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

asset_management_agent = create_agent(
    llm,
    [TokenBalanceTool(), NFTBalanceTool()],
    """
    You are AssetManager, responsible for helping users query and manage their crypto assets,
    including tokens and NFTs. Use the provided tools to fetch the required information accurately and efficiently.
""",
)
