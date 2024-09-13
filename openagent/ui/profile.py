import chainlit as cl

from openagent.conf.llm_provider import TOOL_CALL_MODELS

provider_key_to_profile_info = {
    "gpt-3.5-turbo": {
        "name": "GPT-3.5",
        "markdown_description": "Using **GPT-3.5**.",
        "icon": "https://custom.typingmind.com/assets/models/gpt-35.webp",
    },
    "gpt-4o": {
        "name": "GPT-4o",
        "markdown_description": "Using **GPT-4o**.",
        "icon": "https://custom.typingmind.com/assets/models/gpt-4.webp",
    },
    "gpt-4o-mini": {
        "name": "GPT-4o-mini",
        "markdown_description": "Using **GPT-4o**.",
        "icon": "https://custom.typingmind.com/assets/models/gpt-4.webp",
    },
    "gemini-1.5-pro": {
        "name": "Gemini 1.5 Pro",
        "markdown_description": "Using **Gemini 1.5 Pro**.",
        "icon": "https://custom.typingmind.com/assets/models/gemini.png",
    },
    "gemini-1.5-flash": {
        "name": "Gemini 1.5 Flash",
        "markdown_description": "Using **Gemini 1.5 Flash**.",
        "icon": "https://custom.typingmind.com/assets/models/gemini.png",
    },
}
for model in TOOL_CALL_MODELS:
    provider_key_to_profile_info[model] = {
        "name": model,
        "markdown_description": f"Using **{model}**.",
        "icon": "https://ollama.com/public/ollama.png",
    }


def provider_to_profile(provider_key):
    profile_info = provider_key_to_profile_info.get(provider_key)
    if profile_info:
        return cl.ChatProfile(
            name=profile_info["name"],
            markdown_description=profile_info["markdown_description"],
            icon=profile_info["icon"],
            starters=[
                cl.Starter(
                    label="Swap token",
                    message="Swap 1 ETH for USDC on the Ethereum.",
                    icon="/public/swap.png",
                ),
                cl.Starter(
                    label="Market analysis",
                    message="What's the current price of Ethereum and its market trend?",
                    icon="/public/market.png",
                ),
                cl.Starter(
                    label="Transfer token",
                    message="Can you help me transfer 0.1 ETH to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e on the Ethereum network?",
                    icon="/public/transfer.png",
                ),
                cl.Starter(
                    label="Block explorer",
                    message="What's the latest block height on the Ethereum network, and what are the current gas fees?",
                    icon="/public/block_chain.png",
                ),
            ],
        )
    return None


def profile_name_to_provider_key(name):
    map = {v["name"]: k for k, v in provider_key_to_profile_info.items()}
    return map.get(name)
