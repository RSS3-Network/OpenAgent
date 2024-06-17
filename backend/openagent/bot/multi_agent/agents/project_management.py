from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openagent.bot.multi_agent.agents.agent_factory import create_agent
from openagent.bot.multi_agent.tools.project_tool import ProjectTool
from openagent.bot.multi_agent.tools.tavily_tool import tavily_tool

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

research_analyst_agent = create_agent(
    llm,
    [ProjectTool(), tavily_tool],
    """
You are ResearchAnalyst, responsible for assisting users in conducting research and analysis related to web3 projects.
 Provide accurate and detailed information about project progress, team members, market trends, investors,
 and other relevant data to support investment decisions.
""",
)
