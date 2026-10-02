from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's question or request"
    )


class AIResponse(BaseModel):
    response: str


class HealthResponse(BaseModel):
    status: str
    service: str


class ErrorResponse(BaseModel):
    detail: str