from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.bot.multi_agent.agents.agent_factory import create_agent
from openagent.bot.multi_agent.tools.tavily_tool import tavily_tool
from openagent.experts.feed_expert import FeedExpert

load_dotenv()
llm = ChatOpenAI(model="gpt-4-1106-preview")

feed_agent = create_agent(
    llm,
    [FeedExpert(), tavily_tool],
    "You are an expert in web3 social platforms' activities.",
)
