from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.bot.multi_agent.agents.agent_factory import create_agent
from openagent.bot.multi_agent.tools.tavily_tool import tavily_tool
from openagent.experts.nft_expert import NFTExpert
from openagent.experts.price_expert import PriceExpert

load_dotenv()
llm = ChatOpenAI(model="gpt-4-1106-preview")

market_agent = create_agent(
    llm,
    [tavily_tool, PriceExpert(), NFTExpert()],
    "You are a market analyst specialized in Web3. You provide market "
    "information about CEX, DEX, NFTs, inscriptions, and runes.",
)
