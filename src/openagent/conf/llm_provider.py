from contextvars import ContextVar

import ollama
from langchain_core.language_models import BaseChatModel
from langchain_google_vertexai import ChatVertexAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from loguru import logger
from toolz import memoize

from openagent.conf.env import settings


@memoize
def get_available_ollama_providers():
    try:
        ollama_list = ollama.list()
        models_ = list(map(lambda x: x["name"], ollama_list["models"]))
        all_ = ["llama3.1:latest"]

        available_models = list(filter(lambda x: x in all_, models_))
        return available_models
    except Exception as e:
        logger.error(f"Failed to get available ollama providers: {e}")
        return []


def get_available_providers():
    providers = {}
    if settings.OPENAI_API_KEY:
        providers["gpt-3.5-turbo"] = ChatOpenAI(model="gpt-3.5-turbo")
        providers["gpt-4o"] = ChatOpenAI(model="gpt-4o")
    if settings.VERTEX_PROJECT_ID:
        providers["gemini-1.5-pro"] = ChatVertexAI(model="gemini-1.5-pro")

    if settings.OLLAMA_HOST:
        ollama_providers = get_available_ollama_providers()
        print(ollama_providers)
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
            llm = list(available_providers.values())[0]  # noqa
        else:
            logger.error("No LLM provider is available.")
            raise ValueError("No LLM provider is available.")
    return llm
