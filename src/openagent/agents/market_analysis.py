from dotenv import load_dotenv

from openagent.agents.agent_factory import create_agent
from openagent.conf.llm_provider import get_current_llm
from openagent.tools.coin_market_tool import CoinMarketTool
from openagent.tools.funding_rate_tool import FundingRateTool
from openagent.tools.nft_tool import NFTTool
from openagent.tools.price_tool import PriceTool
from openagent.tools.tavily_tool import tavily_tool

load_dotenv()
llm = get_current_llm()

market_analysis_agent = create_agent(
    llm,
    [tavily_tool, PriceTool(), FundingRateTool(), NFTTool(), CoinMarketTool()],
    """
You are MarketAnalyst, responsible for providing market data analysis.
Help users understand market dynamics and trends by retrieving real-time price information of tokens.

Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
""".strip(),
)
