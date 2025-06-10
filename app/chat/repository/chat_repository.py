
from sqlalchemy.future import select

from app.chat.model.chat import Chat
from internal.config.db_config import DBConfig
from internal.domain.base_repository import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, db_config: DBConfig) -> None:
        super().__init__(Chat, db_config)

    async def find_by_name(self, name: str) -> Chat|None:
        async with self.db_config.getSession() as session:
            stmt = select(self.model_class).filter_by(name=name)
            result = await session.execute(stmt)
            return result.scalars().first()
