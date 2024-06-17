from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.bot.multi_agent.agents.agent_factory import create_agent
from openagent.bot.multi_agent.tools.coin_market_tool import CoinMarketTool
from openagent.bot.multi_agent.tools.tavily_tool import tavily_tool
from openagent.experts.nft_expert import NFTExpert
from openagent.experts.price_expert import PriceExpert

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

market_analysis_agent = create_agent(
    llm,
    [tavily_tool, PriceExpert(), NFTExpert(), CoinMarketTool()],
    """
    You are MarketAnalyst, responsible for providing market data analysis.
    Help users understand market dynamics and trends by retrieving real-time price information of tokens.
""",
)
