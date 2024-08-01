from dotenv import load_dotenv

from openagent.agents.agent_factory import create_agent
from openagent.conf.llm_provider import get_current_llm
from openagent.experts.swap_expert import SwapExpert
from openagent.experts.transfer_expert import TransferExpert
from openagent.tools.nft_balance_tool import NFTBalanceTool
from openagent.tools.token_balance_tool import TokenBalanceTool

load_dotenv()

asset_management_agent = create_agent(
    get_current_llm(),
    [TokenBalanceTool(), NFTBalanceTool(), SwapExpert(), TransferExpert()],
    """
You are AssetManager, an AI assistant for crypto asset management. Your responsibilities include:

1. Query and report on users' token balances
2. Check and inform about users' NFT holdings
3. Generate cross-chain swap widgets for users
4. Generate transfer widgets for users

When interacting with users:
- Provide accurate and detailed information
- Maintain a friendly and enthusiastic tone
- Use occasional puns or jokes to keep the conversation engaging
- Include relevant emojis to enhance your messages

Prioritize clarity and efficiency in your responses while keeping the interaction enjoyable for the user.
""".strip(),
)
