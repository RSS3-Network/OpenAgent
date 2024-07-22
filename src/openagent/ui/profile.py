import chainlit as cl

provider_key_to_profile_info = {
    "gpt-3.5-turbo": {
        "name": "GPT-3.5",
        "markdown_description": "The underlying LLM model is **GPT-3.5**.",
        "icon": "https://custom.typingmind.com/assets/models/gpt-35.webp",
    },
    "gpt-4o": {
        "name": "GPT-4",
        "markdown_description": "The underlying LLM model is **GPT-4**.",
        "icon": "https://custom.typingmind.com/assets/models/gpt-4.webp",
    },
    "gemini-1.5-pro": {
        "name": "Gemini 1.5 Pro",
        "markdown_description": "The underlying LLM model is **Gemini 1.5 Pro**.",
        "icon": "https://custom.typingmind.com/assets/models/gemini.png",
    },
}


def provider_to_profile(provider_key):
    profile_info = provider_key_to_profile_info.get(provider_key)
    if profile_info:
        return cl.ChatProfile(name=profile_info["name"], markdown_description=profile_info["markdown_description"], icon=profile_info["icon"])
    return None


def profile_name_to_provider_key(name):
    map = {v["name"]: k for k, v in provider_key_to_profile_info.items()}
    return map.get(name)
