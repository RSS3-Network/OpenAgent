from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

from openagent.agents.agent_factory import create_agent
from openagent.executors.defi_executor import DeFiExecutor
from openagent.executors.feed_executor import FeedExecutor
from openagent.executors.feed_source_executor import FeedSourceExecutor
from openagent.executors.tg_news_executor import TelegramNewsExecutor

load_dotenv()


def build_feed_explorer_agent(llm: BaseChatModel):
    feed_explorer_agent = create_agent(
        llm,
        [FeedExecutor(), FeedSourceExecutor(), DeFiExecutor(), TelegramNewsExecutor()],
        """
    You are FeedExplorer, specialized in exploring and presenting blockchain activities for specific wallet addresses.

    Use:
    - FeedExecutor & FeedSourceExecutor for social activities
    - DeFiExecutor for DeFi operations
    - TelegramNewsExecutor for latest news context

    Your answer should be detailed and include puns or jokes where possible \
    And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
    """.strip(),
    )
    return feed_explorer_agent
