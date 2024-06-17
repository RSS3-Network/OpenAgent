from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.bot.multi_agent.agents.agent_factory import create_agent
from openagent.bot.multi_agent.tools.tavily_tool import tavily_tool
from openagent.experts.feed_expert import FeedExpert

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

social_track_agent = create_agent(
    llm,
    [FeedExpert(), tavily_tool],
    """
    You are Social Tracker, focused on tracking web3 social media and community interactions.
     Provide users with the latest updates and discussions from the web3 ecosystem.
     Use the available tools to collect and display social content.
""",
)
