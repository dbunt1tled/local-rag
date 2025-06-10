from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import UUID4


class FileBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    name: str | None = Field(default=None, description="File name",)
    chat_id: UUID4 | None = Field(None, description="Chat id",)
    content: bytes | None = Field(None, description="File content",)


class FileCreate(FileBase):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "name": "new_file.pdf",
                "chat_id": "00000000-0000-0000-0000-000000000000",
                "content": "bytes content"
            }
        }
    )
    name: str = Field(..., description="File name",)
    chat_id: UUID4 = Field(..., description="Chat Id",)
    content: bytes = Field(..., description="File content",)


class FileUpdate(FileBase):
    name: str|None = Field(None, min_length=3, max_length=50)

class FileResponse(FileBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    name: str
    chat_id: UUID4
    content: bytes
    created_at: datetime
    updated_at: datetime

