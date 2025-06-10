

from app.message.model.message import Message
from internal.config.db_config import DBConfig
from internal.domain.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self, db_config: DBConfig) -> None:
        super().__init__(Message, db_config)
