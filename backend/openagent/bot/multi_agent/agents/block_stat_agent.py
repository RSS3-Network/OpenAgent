from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.bot.multi_agent.agents.agent_factory import create_agent
from openagent.bot.multi_agent.tools.tavily_tool import tavily_tool
from openagent.experts.block_stat_expert import BlockStatExpert

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

block_stat_agent = create_agent(
    llm,
    [BlockStatExpert(), tavily_tool],
    "You are an expert in blockchain statistics, known the block height, hash, gas fee etc.",
)
