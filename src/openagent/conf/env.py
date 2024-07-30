from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Database connection string (required)
    DB_CONNECTION: str = Field(..., description="Database connection string (required)")

    # LLM provider settings: at least one provider must be set
    VERTEX_PROJECT_ID: Optional[str] = Field(default=None, description="Google Cloud Vertex project ID (optional)")
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key (optional)")
    GOOGLE_GEMINI_API_KEY: Optional[str] = Field(default=None, description="Google Gemini API Key (optional)")
    OLLAMA_API_BASE: Optional[str] = Field(default=None, description="OLLAMA API Base URL (optional)")

    # API keys for various tools; some features will be disabled if not set
    NFTSCAN_API_KEY: Optional[str] = Field(default=None, description="NFTScan API Key (optional)")
    COVALENT_API_KEY: Optional[str] = Field(default=None, description="Covalent API Key (optional)")
    ROOTDATA_API_KEY: Optional[str] = Field(default=None, description="RootData API Key (optional)")
    COINGECKO_API_KEY: Optional[str] = Field(default=None, description="CoinGecko API Key (optional)")
    RSS3_DATA_API: str = Field(default="https://gi.rss3.io", description="RSS3 Data API URL (optional)")
    RSS3_SEARCH_API: str = Field(default="https://devnet.rss3.io/search", description="RSS3 Search API URL (optional)")

    # Chainlit OAuth settings; either all fields are None or all are set
    CHAINLIT_AUTH_SECRET: Optional[str] = Field(default=None, description="Chainlit Auth Secret")
    OAUTH_AUTH0_CLIENT_ID: Optional[str] = Field(default=None, description="OAuth Auth0 Client ID")
    OAUTH_AUTH0_CLIENT_SECRET: Optional[str] = Field(default=None, description="OAuth Auth0 Client Secret")
    OAUTH_AUTH0_DOMAIN: Optional[str] = Field(default=None, description="OAuth Auth0 Domain")


settings = Settings()
