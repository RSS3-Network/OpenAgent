from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

from openagent.agents.agent_factory import create_agent
from openagent.conf.env import settings
from openagent.executors.project_executor import ProjectExecutor
from openagent.executors.search_executor import search_executor

load_dotenv()


def build_research_analyst_agent(llm: BaseChatModel):
    executors = [search_executor]
    if settings.ROOTDATA_API_KEY:
        executors.append(ProjectExecutor())

    research_analyst_agent = create_agent(
        llm,
        executors,
        """
    You are ResearchAnalyst, responsible for assisting users in conducting research and analysis related to web3 projects.
     Provide accurate and detailed information about project progress, team members, market trends, investors,
     and other relevant data to support investment decisions.

    Your answer should be detailed and include puns or jokes where possible \
    And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.
    """.strip(),
    )
    return research_analyst_agent
