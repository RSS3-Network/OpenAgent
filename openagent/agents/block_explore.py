from dotenv import load_dotenv

from openagent.agents.agent_factory import create_agent
from openagent.conf.llm_provider import get_current_llm
from openagent.executors.block_stat_executor import BlockStatExecutor
from openagent.executors.search_executor import search_executor

load_dotenv()

executors = [BlockStatExecutor(), search_executor]


block_explorer_agent = create_agent(
    get_current_llm(),
    executors,
    """
You are BlockExplorer, dedicated to exploring and presenting detailed blockchain information.
Help users query transaction details, block data, gas fees, block height, and other blockchain-related information.
Use the available tools to gather and display accurate blockchain data.

Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
""".strip(),
)
