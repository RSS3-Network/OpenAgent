from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_CONNECTION: str = Field(..., description="Database connection string")

    # LLM provider settings (at least one required)
    VERTEX_PROJECT_ID: Optional[str] = Field(
        default=None, description="Google Cloud Vertex project ID. Info: https://cloud.google.com/vertex-ai/docs/reference"
    )
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key. Info: https://platform.openai.com")
    GOOGLE_GEMINI_API_KEY: Optional[str] = Field(default=None, description="Google Gemini API Key. Info: https://ai.google.dev")
    OLLAMA_HOST: Optional[str] = Field(default=None, description="OLLAMA API Base URL. Info: https://github.com/ollama/ollama")

    # API keys for various tools; some features will be disabled if not set
    NFTSCAN_API_KEY: Optional[str] = Field(default=None, description="NFTScan API Key. Info: https://nftscan.com/")
    COVALENT_API_KEY: Optional[str] = Field(default=None, description="Covalent API Key. Info: https://goldrush.dev/docs/api/")
    ROOTDATA_API_KEY: Optional[str] = Field(default=None, description="RootData API Key. Info: https://www.rootdata.com/")
    COINGECKO_API_KEY: Optional[str] = Field(default=None, description="CoinGecko API Key. Info: https://www.coingecko.com/en/api/pricing")
    RSS3_DATA_API: str = Field(default="https://gi.rss3.io", description="RSS3 Data API URL")
    RSS3_SEARCH_API: str = Field(default="https://devnet.rss3.io/search", description="RSS3 Search API URL")

    # Chainlit OAuth settings; either all fields are None or all are set
    CHAINLIT_AUTH_SECRET: Optional[str] = Field(default=None, description="Chainlit Auth Secret")
    OAUTH_AUTH0_CLIENT_ID: Optional[str] = Field(default=None, description="OAuth Auth0 Client ID")
    OAUTH_AUTH0_CLIENT_SECRET: Optional[str] = Field(default=None, description="OAuth Auth0 Client Secret")
    OAUTH_AUTH0_DOMAIN: Optional[str] = Field(default=None, description="OAuth Auth0 Domain")


settings = Settings()
