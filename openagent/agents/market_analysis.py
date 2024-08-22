from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

from openagent.agents.agent_factory import create_agent
from openagent.conf.env import settings
from openagent.executors.coin_market_executor import CoinMarketExecutor
from openagent.executors.funding_rate_executor import FundingRateExecutor
from openagent.executors.nft_rank_executor import NFTRankingExecutor
from openagent.executors.price_executor import PriceExecutor
from openagent.executors.search_executor import search_executor

load_dotenv()


def build_market_analysis_agent(llm: BaseChatModel):
    executors = [FundingRateExecutor(), search_executor]
    if settings.COINGECKO_API_KEY:
        executors.extend([PriceExecutor(), CoinMarketExecutor()])
    if settings.MORALIS_API_KEY:
        executors.extend([NFTRankingExecutor()])
    return create_agent(
        llm,
        executors,
        """
    You are MarketAnalyst, responsible for providing market data analysis.
    Help users understand market dynamics and trends by retrieving real-time price information of tokens.

    Your answer should be detailed and include puns or jokes where possible \
    And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
    """.strip(),
    )
