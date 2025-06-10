import uuid
from dataclasses import dataclass
from typing import Sequence

from app.chat.dto.chat_schema import ChatCreate
from app.chat.model.chat import Chat
from app.chat.repository.chat_repository import ChatRepository


@dataclass
class ChatService:
    chat_repository: ChatRepository

    async def create(self, chat_create: ChatCreate) -> Chat:
        chat = Chat(name=chat_create.name)
        return await self.chat_repository.create(chat)

    async def all(self) -> Sequence[Chat]:
        return await self.chat_repository.all()

    async def get_by_id(self, chat_id: uuid.UUID) -> Chat:
        return await self.chat_repository.get_by_id(chat_id)

    async def delete(self, chat_id: uuid.UUID) -> bool:
        return await self.chat_repository.delete(chat_id)
