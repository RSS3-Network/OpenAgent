from dotenv import load_dotenv
from openagent.agents.agent_factory import create_agent
from openagent.conf.llm_provider import get_current_llm
from openagent.tools.block_stat_tool import BlockStatTool
from openagent.tools.tavily_tool import tavily_tool
from openagent.experts.defi_expert import DeFiExpert
from openagent.experts.feed_expert import FeedExpert
from openagent.experts.feed_source_expert import FeedSourceExpert

load_dotenv()

block_explorer_agent = create_agent(
    get_current_llm(),
    [BlockStatTool(), tavily_tool, FeedExpert(),FeedSourceExpert(), DeFiExpert()],
    """
You are BlockExplorer, dedicated to exploring and presenting detailed blockchain information.
Help users query transaction details, block data, gas fees, block height, and other blockchain-related information.
Use the available tools to gather and display accurate blockchain data.

In addition to blockchain data, leverage the FeedExpert to provide insights on various feeds, the FeedSourceExpert 
to retrieve activities based on different sources, and the DeFiExpert to give detailed information on DeFi activities.


Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
""".strip(),
)
