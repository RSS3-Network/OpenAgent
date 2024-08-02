from contextvars import ContextVar

import ollama
from langchain_core.language_models import BaseChatModel
from langchain_google_vertexai import ChatVertexAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from loguru import logger
from toolz import memoize

from openagent.conf.env import settings

TOOL_CALL_MODELS = [
    "llama3.1",
    "mistral-nemo",
    "mistral",
    "mistral-large",
    "mixtral",
    "command-r-plus",
    "deepseek-coder-v2",
    "llama3-groq-tool-use",
    "firefunction-v2",
]


@memoize
def get_available_ollama_providers():
    try:
        ollama_list = ollama.list()
        models_ = list(map(lambda x: x["name"].split(":")[0], ollama_list["models"]))
        available_models = list(filter(lambda x: x in TOOL_CALL_MODELS, models_))
        return available_models
    except Exception:
        logger.warning("Failed to get available ollama providers")
        return []


def get_available_providers():
    providers = {}
    if settings.OPENAI_API_KEY:
        providers["gpt-3.5-turbo"] = ChatOpenAI(model="gpt-3.5-turbo")
        providers["gpt-4o"] = ChatOpenAI(model="gpt-4o")
    if settings.VERTEX_PROJECT_ID:
        providers["gemini-1.5-pro"] = ChatVertexAI(model="gemini-1.5-pro")
        providers["gemini-1.5-flash"] = ChatVertexAI(model="gemini-1.5-flash")

    if settings.OLLAMA_HOST:
        ollama_providers = get_available_ollama_providers()
        for model in ollama_providers:
            providers[model] = ChatOllama(model=model)
    return providers


_current_llm_provider: ContextVar[BaseChatModel | None] = ContextVar("current_llm_provider", default=None)


def set_current_llm(provider_name: str):
    logger.info(f"Setting current LLM provider to {provider_name}")
    providers = get_available_providers()
    _current_llm_provider.set(providers.get(provider_name))


def get_current_llm() -> BaseChatModel | None:
    llm = _current_llm_provider.get()
    if llm is None:
        available_providers = get_available_providers()
        if len(available_providers) > 0:
            logger.warning(f"No LLM provider is set. Using the {list(available_providers.keys())[0]} provider.")  # noqa
            llm = list(available_providers.values())[0]  # noqa
        else:
            logger.error("No LLM provider is available.")
            raise ValueError("No LLM provider is available.")
    return llm
