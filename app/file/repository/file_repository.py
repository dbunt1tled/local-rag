from app.file.model.file import File
from internal.config.db_config import DBConfig
from internal.domain.base_repository import BaseRepository


class FileRepository(BaseRepository[File]):
    def __init__(self, db_config: DBConfig) -> None:
        super().__init__(File, db_config)
