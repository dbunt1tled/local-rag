from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    answer: str | None = Field(default=None, description="Answer on the question",)