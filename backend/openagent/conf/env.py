from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MODEL_NAME: str = Field(default="llava:13b", env="MODEL_NAME")
    LLM_API_BASE: str = Field(..., env="LLM_API_BASE")
    GOOGLE_API_KEY: Optional[str] = Field(default=None)
    NFTSCAN_API_KEY: str = Field(..., env="NFTSCAN_API_KEY")
    BIZ_DB_CONNECTION: str = Field(..., env="BIZ_DB_CONNECTION")
    VEC_DB_CONNECTION: str = Field(..., env="VEC_DB_CONNECTION")
    RSS3_DATA_API: str = Field(default="https://testnet.rss3.io/data", env="RSS3_DATA_API")
    RSS3_SEARCH_API: str = Field(default="https://devnet.rss3.io/search", env="RSS3_SEARCH_API")
    TG_API_ID: str = Field(..., env="TG_API_ID")
    TG_API_HASH: str = Field(..., env="TG_API_HASH")
    TG_BOT_TOKEN: str = Field(..., env="TG_BOT_TOKEN")
    COVALENT_API_KEY: str = Field(..., env="COVALENT_API_KEY")
    ROOTDATA_API_KEY: str = Field(..., env="ROOTDATA_API_KEY")


settings = Settings()
