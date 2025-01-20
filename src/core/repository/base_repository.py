from typing import List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.base_model import Base


DB = TypeVar("DB", bound=Base)
P = TypeVar("P", bound=BaseModel)


class BaseRepository:
    """
    Базовый репозиторий для работы с данными в базе данных.

    Attributes:
        session (AsyncSession): Сессия базы данных.
        model (Type[DB]): Модель данных.
    """

    def __init__(self, session: AsyncSession, model: Type[DB]):
        self.session = session
        self.model = model

    async def get_obj_by_id(self, obj_id: int) -> DB | None:
        """
        Получение объекта из базы данных по id.

        Args:
            obj_id (int): id объекта.

        Returns:
            DB: Объект из базы данных.
            None: Если объект не найден.
        """
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.scalars(stmt)

        return result.one_or_none()

    async def get_all_obj(self) -> List[DB]:
        """
        Получение всех объектов из базы данных.

        Returns:
            List[DB]: Список объектов из базы данных.
        """
        stmt = select(self.model)
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def create(self, obj_in: P) -> DB | bool:
        """
        Создание новой записи в базе данных.

        Args:
            obj_in (P): Данные для создания новой записи.

        Returns:
            DB: Созданный объект.
            False: Если объект не создан (уже существует в базе данных).
        """
        obj = self.model(**obj_in.model_dump())
        self.session.add(obj)
        try:
            await self.session.commit()
            return obj

        except IntegrityError:
            return False

    async def update(self, obj_id: int, obj_in: P) -> DB | bool:
        """
        Обновление объекта в базе данных.

        Args:
            obj_id (int): id изменяемого объекта.
            obj_in (P): Данные для обновления объекта.

        Returns:
            DB: Обновленный объект.
            False: Если объект не был обновлён (не найден в базе данных).
        """
        stmt = update(self.model).filter_by(id=obj_id).values(**obj_in.model_dump())
        result = await self.session.execute(stmt)
        if result.rowcount != 0:
            await self.session.commit()
            return await self.get_obj_by_id(obj_id=obj_id)

        await self.session.rollback()
        return False

    async def delete(self, obj_id: int) -> bool | DB:
        """
        Удаление объекта из базы данных.

        Args:
            obj_id (int): id объекта для удаления.

        Returns:
            DB: Модель удалённого объекта.
            False: Если объект не был удалён (не найден в базе данных).
        """
        stmt = delete(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        deleted_count = result.rowcount
        if deleted_count == 1:
            await self.session.commit()
            return self.model

        await self.session.rollback()
        return False
