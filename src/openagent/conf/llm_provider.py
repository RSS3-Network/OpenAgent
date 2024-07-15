import os

from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
from dotenv import load_dotenv

from openagent.conf.env import settings


def build_providers():
    providers = {}
    if settings.OPENAI_API_KEY:
        providers['gpt-3.5-turbo'] = ChatOpenAI(model="gpt-3.5-turbo")
        providers['gpt-4o'] = ChatOpenAI(model="gpt-4o")

    if settings.VERTEX_PROJECT_ID:
        providers['gemini-1.5-pro'] = ChatVertexAI(model="gemini-1.5-pro")
    return providers


if __name__ == '__main__':
    print(build_providers())
