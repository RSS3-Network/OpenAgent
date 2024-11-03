from typing import Dict, List

import ollama
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from loguru import logger
from toolz import memoize

from openagent.conf.env import settings

SUPPORTED_MODELS = {
    "llama3.2": {"name": "llama3.2", "supports_tools": True},
    "mistral-nemo": {"name": "mistral-nemo", "supports_tools": True},
    "darkmoon/olmo:7B-instruct-q6-k": {"name": "olmo", "supports_tools": False},
}

MODELS_ICONS = {
    "llama3.1": "/public/llama.png",
    "llama3.2": "/public/llama.png",
    "mistral": "/public/mistral.png",
    "mistral-nemo": "/public/mistral.png",
    "mistral-large": "/public/mistral.png",
    "olmo": "/public/olmo.png",
}


@memoize
def get_available_ollama_providers() -> List[str]:
    try:
        ollama_list = ollama.list()
        available_models = []
        for model in ollama_list["models"]:
            full_name = model["name"]
            # check if the full model name is in SUPPORTED_MODELS
            if full_name in SUPPORTED_MODELS:
                available_models.append(full_name)
            else:
                # try to check the base name (without version tag)
                base_name = full_name.split(":")[0]
                if base_name in SUPPORTED_MODELS:
                    available_models.append(base_name)
        return available_models
    except Exception as e:
        logger.exception("Failed to get available ollama providers", e)
        return []


def get_provider(model: str, provider_func) -> Dict[str, BaseChatModel]:
    provider = provider_func(model)
    return {model: provider} if provider else {}


def get_available_providers() -> Dict[str, BaseChatModel]:
    providers = {}

    provider_configs = [
        (["gpt-4o-mini", "gpt-4o"], get_openai_provider),
        (["gemini-1.5-pro", "gemini-1.5-flash"], get_gemini_provider),
    ]

    for models, provider_func in provider_configs:
        for model in models:
            providers.update(get_provider(model, provider_func))

    if settings.OLLAMA_HOST:
        ollama_models = get_available_ollama_providers()
        for model in ollama_models:
            providers.update(get_provider(model, get_ollama_provider))

    return providers


def get_openai_provider(model: str) -> BaseChatModel | None:
    return ChatOpenAI(model=model) if settings.OPENAI_API_KEY else None


def get_gemini_provider(model: str) -> BaseChatModel | None:
    if settings.VERTEX_PROJECT_ID:
        return ChatVertexAI(model=model)
    elif settings.GOOGLE_GEMINI_API_KEY:
        return ChatGoogleGenerativeAI(model=model, google_api_key=settings.GOOGLE_GEMINI_API_KEY)
    return None


def get_ollama_provider(model: str) -> BaseChatModel | None:
    return ChatOllama(model=model) if settings.OLLAMA_HOST else None
