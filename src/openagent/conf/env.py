from typing import List, Optional

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # PGVector connection string
    DB_CONNECTION: str = Field(..., env="DB_CONNECTION", description="PGVector connection string")

    # Online LLM API KEY
    VERTEX_PROJECT_ID: Optional[str] = Field(default=None, description="Google cloud vertex project id (optional)")
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY", description="OpenAI API Key (optional)")
    # Local LLM configuration
    OLLAMA_MODEL: Optional[List[str]] = Field(default=None, env="OLLAMA_MODEL", description="OLLAMA Model list (optional)")
    OLLAMA_MODEL_URL: Optional[str] = Field(default=None, env="OLLAMA_MODEL_URL", description="OLLAMA Model URL (optional)")

    # Tool API Keys
    NFTSCAN_API_KEY: Optional[str] = Field(..., env="NFTSCAN_API_KEY", description="NFTScan API Key (optional)")
    RSS3_DATA_API: Optional[str] = Field(
        default="https://testnet.rss3.io/data", env="RSS3_DATA_API", description="RSS3 Data API with a default value"
    )
    RSS3_SEARCH_API: Optional[str] = Field(
        default="https://devnet.rss3.io/search", env="RSS3_SEARCH_API", description="RSS3 Search API with a default value"
    )
    COVALENT_API_KEY: Optional[str] = Field(..., env="COVALENT_API_KEY")
    ROOTDATA_API_KEY: Optional[str] = Field(..., env="ROOTDATA_API_KEY")
    COINGECKO_API_KEY: Optional[str] = Field(..., env="COINGECKO_API_KEY")

    # Validator to split comma-separated string into a list
    @field_validator("OLLAMA_MODEL", mode="before")
    def split_string(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v


settings = Settings()
