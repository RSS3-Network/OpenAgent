from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MODEL_NAME: str = Field(default="gemini-1.5-pro", env="MODEL_NAME")
    LLM_API_BASE: Optional[str] = Field(default=None)
    PROJECT_ID: Optional[str] = Field(default=None)
    NFTSCAN_API_KEY: str = Field(..., env="NFTSCAN_API_KEY")
    BIZ_DB_CONNECTION: str = Field(..., env="BIZ_DB_CONNECTION")
    VEC_DB_CONNECTION: str = Field(..., env="VEC_DB_CONNECTION")
    RSS3_DATA_API: str = Field(default="https://testnet.rss3.io/data", env="RSS3_DATA_API")
    RSS3_SEARCH_API: str = Field(default="https://devnet.rss3.io/search", env="RSS3_SEARCH_API")
    WIDGET_URL: str = Field(default="http://localhost:8001", env="WIDGET_URL")


settings = Settings()
