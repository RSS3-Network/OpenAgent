from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.agents.agent_factory import create_agent
from openagent.conf.llm_provider import get_current_llm
from openagent.tools.nft_balance_tool import NFTBalanceTool
from openagent.tools.token_balance_tool import TokenBalanceTool

load_dotenv()

asset_management_agent = create_agent(
    get_current_llm(),
    [TokenBalanceTool(), NFTBalanceTool()],
    """
You are AssetManager, responsible for helping users query and manage their crypto assets,
including tokens and NFTs. Use the provided tools to fetch the required information accurately and efficiently.

Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
""".strip(),
)
