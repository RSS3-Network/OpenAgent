from contextvars import ContextVar

from langchain_core.language_models import BaseChatModel
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI
from loguru import logger

from openagent.conf.env import settings


def get_available_providers():
    providers = {}
    if settings.OPENAI_API_KEY:
        providers['gpt-3.5-turbo'] = ChatOpenAI(model="gpt-3.5-turbo")
        providers['gpt-4o'] = ChatOpenAI(model="gpt-4o")
    if settings.VERTEX_PROJECT_ID:
        providers['gemini-1.5-pro'] = ChatVertexAI(model="gemini-1.5-pro")
    return providers


_current_llm_provider: ContextVar[BaseChatModel | None] = ContextVar("current_llm_provider", default=None)


def set_current_llm(provider_name: str):
    logger.info(f"Setting current LLM provider to {provider_name}")
    providers = get_available_providers()
    _current_llm_provider.set(providers.get(provider_name))


def get_current_llm() -> BaseChatModel | None:
    return _current_llm_provider.get()
