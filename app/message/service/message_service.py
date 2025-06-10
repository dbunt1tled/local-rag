import uuid
from dataclasses import dataclass
from typing import Sequence

from app.message.dto.message_schema import MessageCreate
from app.message.model.message import Message
from app.message.repository.message_repository import MessageRepository


@dataclass
class MessageService:
    message_repository: MessageRepository

    async def create(self, chat_create: MessageCreate) -> Message:
        chat = Message(
            text=chat_create.text,
            chat_id=chat_create.chat_id,
            type=chat_create.type
        )
        return await self.message_repository.create(chat)

    async def all(self, conditions: dict = {}) -> Sequence[Message]:
        return await self.message_repository.all(conditions=conditions)

    async def get_by_id(self, message_id: uuid.UUID) -> Message:
        return await self.message_repository.get_by_id(message_id)

    async def delete(self, message_id: uuid.UUID) -> bool:
        return await self.message_repository.delete(message_id)

