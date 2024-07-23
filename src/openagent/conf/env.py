from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MODEL_NAME: str = Field(default="gemini-1.5-pro", env="MODEL_NAME")
    LLM_API_BASE: Optional[str] = Field(default=None)
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = Field(default=None)
    GOOGLE_GEMINI_API_KEY: Optional[str] = Field(default=None)
    NFTSCAN_API_KEY: str = Field(..., env="NFTSCAN_API_KEY")
    DB_CONNECTION: str = Field(..., env="DB_CONNECTION")
    RSS3_DATA_API: str = Field(default="https://gi.rss3.io", env="RSS3_DATA_API")
    RSS3_SEARCH_API: str = Field(default="https://devnet.rss3.io/search", env="RSS3_SEARCH_API")

    CHAINLIT_AUTH_SECRET: Optional[str] = Field(default=None, env="CHAINLIT_AUTH_SECRET")
    OAUTH_AUTH0_CLIENT_ID: Optional[str] = Field(default=None, env="OAUTH_AUTH0_CLIENT_ID")
    OAUTH_AUTH0_CLIENT_SECRET: Optional[str] = Field(default=None, env="OAUTH_AUTH0_CLIENT_SECRET")
    OAUTH_AUTH0_DOMAIN: Optional[str] = Field(default=None, env="OAUTH_AUTH0_DOMAIN")


settings = Settings()
