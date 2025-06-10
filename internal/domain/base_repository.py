import uuid
from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy.future import select

from internal.config.db_config import DBConfig
from internal.domain.entity import Entity

T = TypeVar('T', bound=Entity)

class BaseRepository(Generic[T]):

    def __init__(self, model_class: Type[T], db_config: DBConfig):
        self.model_class = model_class
        self.db_config = db_config

    async def create(self, entity: T) -> T:
        async with self.db_config.getSession() as session:
            session.add(entity)
            await session.flush()
            await session.refresh(entity)
            return entity

    async def find_by_id(self, entity_id: uuid.UUID) -> T|None:
        async with self.db_config.getSession() as session:
            stmt = select(self.model_class).filter_by(id=entity_id)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def get_by_id(self, entity_id: uuid.UUID) -> T:
        entity = await self.find_by_id(entity_id=entity_id)
        if entity is None:
            raise ValueError(f"Entity with id {entity_id} not found")
        return entity

    async def all(self, conditions: dict = {}) -> Sequence[T]:
        async with self.db_config.getSession() as session:
            stmt = select(self.model_class).filter_by(**conditions)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def update(self, entity_id: uuid.UUID, data: dict[str, Any]) -> T|None:
        async with self.db_config.getSession() as session:
            entity = await self.get_by_id(entity_id=entity_id)

            for key, value in data.items():
                setattr(entity, key, value)
            await session.flush()
            await session.refresh(entity)
            return entity

    async def delete(self, entity_id: uuid.UUID) -> bool:
        async with self.db_config.getSession() as session:
            entity = await self.get_by_id(entity_id=entity_id)

            await session.delete(entity)
            await session.flush()
            return True
