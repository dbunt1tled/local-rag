import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.message.dto.message_enum import MessageType
from internal.domain.entity import Entity


class Message(Entity):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    text: Mapped[str] = mapped_column(Text(), nullable=False)
    chat_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    type: Mapped[MessageType] = mapped_column(Enum(MessageType), default=MessageType.USER, nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, text='{self.text}', chat_id='{self.chat_id}', type='{self.type}', updated_at='{self.updated_at}', created_at='{self.created_at}')>"
