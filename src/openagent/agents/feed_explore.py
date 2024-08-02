from dotenv import load_dotenv

from openagent.agents.agent_factory import create_agent
from openagent.conf.llm_provider import get_current_llm
from openagent.experts.defi_expert import DeFiExpert
from openagent.experts.feed_expert import FeedExpert
from openagent.experts.feed_source_expert import FeedSourceExpert

load_dotenv()

feed_explorer_agent = create_agent(
    get_current_llm(),
    [FeedExpert(), FeedSourceExpert(), DeFiExpert()],
    """
You are FeedExplorer, dedicated to exploring and presenting blockchain-related
activities and feeds.
Help users query various feeds, retrieve activities from different sources, and provide
insights on DeFi activities.

Leverage the FeedExpert to provide insights on various feeds, the FeedSourceExpert
to retrieve activities based on different sources, and the DeFiExpert to give detailed
information on DeFi activities.

Use the available tools to gather and display accurate feed and activity data.

Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
""".strip(),
)
