from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.bot.multi_agent.agents.agent_factory import create_agent
from openagent.bot.multi_agent.tools.tavily_tool import tavily_tool

load_dotenv()
llm = ChatOpenAI(model="gpt-4-1106-preview")

wallet_agent = create_agent(
    llm,
    [tavily_tool],
    "You are an expert in web3 wallets, known the asset of a wallet in different chains.",
)
