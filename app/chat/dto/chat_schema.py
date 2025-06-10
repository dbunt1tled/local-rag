from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import UUID4


class ChatBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    name: str | None = Field(
        default=None,
        description="Chat name",
    )


class ChatCreate(ChatBase):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "name": "new_chat",
            }
        }
    )
    name: str = Field(..., description="Chat name",)


class ChatUpdate(ChatBase):
    name: str|None = Field(None, min_length=3, max_length=50)

class ChatResponse(ChatBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    created_at: datetime
    updated_at: datetime

