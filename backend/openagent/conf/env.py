from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MODEL_NAME: str = Field(default="llava:13b", env="MODEL_NAME")
    LLM_API_BASE: str = Field(..., env="LLM_API_BASE")
    RSS3_AI_API_BASE: str = Field(..., env="RSS3_AI_API_BASE")
    EXECUTOR_API: str = Field(..., env="EXECUTOR_API")
    NFTSCAN_API_KEY: str = Field(..., env="NFTSCAN_API_KEY")
    BIZ_DB_CONNECTION: str = Field(..., env="BIZ_DB_CONNECTION")
    VEC_DB_CONNECTION: str = Field(..., env="VEC_DB_CONNECTION")


settings = Settings()
