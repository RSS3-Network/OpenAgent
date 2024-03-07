from pydantic import BaseModel, Field


class ErrorResp(BaseModel):
    code: int
    data: object = Field(default="")
    message: str
