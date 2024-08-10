from dotenv import load_dotenv

from openagent.agents.agent_factory import create_agent
from openagent.conf.env import settings
from openagent.conf.llm_provider import get_current_llm
from openagent.executors.coin_market_executor import CoinMarketExecutor
from openagent.executors.funding_rate_executor import FundingRateExecutor
from openagent.executors.nft_rank_executor import NFTRankingExecutor
from openagent.executors.nft_search_executor import NFTSearchExecutor
from openagent.executors.price_executor import PriceExecutor
from openagent.executors.search_executor import search_executor

load_dotenv()

executors = [FundingRateExecutor(), search_executor]
if settings.COINGECKO_API_KEY:
    executors.extend([PriceExecutor(), CoinMarketExecutor()])
if settings.NFTSCAN_API_KEY:
    executors.extend([NFTSearchExecutor(), NFTRankingExecutor()])

market_analysis_agent = create_agent(
    get_current_llm(),
    executors,
    """
You are MarketAnalyst, responsible for providing market data analysis.
Help users understand market dynamics and trends by retrieving real-time price information of tokens.

Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
""".strip(),
)
