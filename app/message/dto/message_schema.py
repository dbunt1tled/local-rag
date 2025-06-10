from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pydantic.types import UUID4

from app.message.dto.message_enum import MessageType


class MessageBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    text: str | None = Field(default=None, description="Content",)
    chat_id: UUID4 | None = Field(None, description="Chat id",)
    type: MessageType | None = Field(None, description="Message type",)


class MessageCreate(MessageBase):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "text": "Hello world",
                "chat_id": "00000000-0000-0000-0000-000000000000",
                "type": "USER"
            }
        }
    )
    text: str = Field(..., description="Chat name",)
    chat_id: UUID4 = Field(..., description="Chat Id",)
    type: MessageType = Field(default=MessageType.USER, description="Message type",)


class MessageUpdate(MessageBase):
    text: str|None = Field(None, min_length=3, max_length=3000)

class ChatResponse(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    created_at: datetime
    updated_at: datetime

