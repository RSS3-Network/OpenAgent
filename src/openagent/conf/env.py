from typing import List, Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_CONNECTION: str = Field(..., env="DB_CONNECTION")

    # Online LLM API KEY
    VERTEX_PROJECT_ID: Optional[str] = Field(default=None, description="Google cloud vertex project id (optional)")
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY", description="OpenAI API Key (optional)")
    # Local LLM configuration
    OLLAMA_MODEL: Optional[List[str]] = Field(default=None, env="OLLAMA_MODEL", description="OLLAMA Model list (optional)")
    OLLAMA_MODEL_URL: Optional[str] = Field(default=None, env="OLLAMA_MODEL_URL", description="OLLAMA Model URL (optional)")


    GOOGLE_GEMINI_API_KEY: Optional[str] = Field(default=None)

    NFTSCAN_API_KEY: Optional[str] = Field(..., env="NFTSCAN_API_KEY", description="NFTScan API Key (optional)")
    COVALENT_API_KEY: Optional[str] = Field(..., env="COVALENT_API_KEY")
    ROOTDATA_API_KEY: Optional[str] = Field(..., env="ROOTDATA_API_KEY")
    COINGECKO_API_KEY: Optional[str] = Field(..., env="COINGECKO_API_KEY")
    RSS3_DATA_API: str = Field(default="https://gi.rss3.io", env="RSS3_DATA_API")
    RSS3_SEARCH_API: str = Field(default="https://devnet.rss3.io/search", env="RSS3_SEARCH_API")

    CHAINLIT_AUTH_SECRET: Optional[str] = Field(default=None, env="CHAINLIT_AUTH_SECRET")
    OAUTH_AUTH0_CLIENT_ID: Optional[str] = Field(default=None, env="OAUTH_AUTH0_CLIENT_ID")
    OAUTH_AUTH0_CLIENT_SECRET: Optional[str] = Field(default=None, env="OAUTH_AUTH0_CLIENT_SECRET")
    OAUTH_AUTH0_DOMAIN: Optional[str] = Field(default=None, env="OAUTH_AUTH0_DOMAIN")


settings = Settings()
