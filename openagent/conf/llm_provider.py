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

TOOL_CALL_MODELS = [
    "llama3.2",
    "mistral-nemo",
    "mistral",
    "mistral-large",
    "mixtral",
    "command-r-plus",
    "deepseek-coder-v2",
    "llama3-groq-tool-use",
    "firefunction-v2",
]


def get_available_ollama_providers() -> List[str]:
    try:
        ollama_list = ollama.list()
        models_ = [model["name"].split(":")[0] for model in ollama_list["models"]]
        return [model for model in models_ if model in TOOL_CALL_MODELS]
    except Exception as e:
        logger.warning("Failed to get available ollama providers",e)
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
