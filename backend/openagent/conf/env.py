from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MODEL_NAME: str = Field(default="llava:13b", env="MODEL_NAME")
    LLM_API_BASE: str = Field(..., env="LLM_API_BASE")
    RSS3_AI_API_BASE: str = Field(..., env="RSS3_AI_API_BASE")
    EXECUTOR_API: str = Field(..., env="EXECUTOR_API")
    POSTGRES_SERVER: str = Field(..., env="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_CONNECTION_STRING: str = ""
    NFTSCAN_API_KEY: str = Field(..., env="NFTSCAN_API_KEY")

    def postgres_connection_string(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}\
@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"


settings = Settings()
