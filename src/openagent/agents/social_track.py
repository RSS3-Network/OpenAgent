from dotenv import load_dotenv

from openagent.agents.agent_factory import create_agent
from openagent.conf.llm_provider import get_current_llm
from openagent.tools.feed_tool import FeedTool
from openagent.tools.tavily_tool import tavily_tool

load_dotenv()
llm = get_current_llm()

social_track_agent = create_agent(
    llm,
    [FeedTool(), tavily_tool],
    """

You are Social Tracker, focused on tracking web3 social media and community interactions.
 Provide users with the latest updates and discussions from the web3 ecosystem.
 Use the available tools to collect and display social content.
Your answer should be detailed and include puns or jokes where possible \
And keep a lively, enthusiastic, and energetic tone, maybe include some emojis.

""".strip(),
)
