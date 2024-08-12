from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

from openagent.agents.agent_factory import create_agent
from openagent.executors.defi_executor import DeFiExecutor
from openagent.executors.feed_executor import FeedExecutor
from openagent.executors.feed_source_executor import FeedSourceExecutor

load_dotenv()


def build_feed_explorer_agent(llm: BaseChatModel):
    feed_explorer_agent = create_agent(
        llm,
        [FeedExecutor(), FeedSourceExecutor(), DeFiExecutor()],
        """
    You are FeedExplorer, dedicated to exploring and presenting blockchain-related
    activities and feeds.
    Help users query various feeds, retrieve activities from different sources, and provide
    insights on DeFi activities.
    
    Leverage the FeedExecutor to provide insights on various feeds, the FeedSourceExecutor
    to retrieve activities based on different sources, and the DeFiExecutor to give detailed
    information on DeFi activities.
    
    Use the available tools to gather and display accurate feed and activity data.
    
    Your answer should be detailed and include puns or jokes where possible \
    And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
    """.strip(),
    )
    return feed_explorer_agent
