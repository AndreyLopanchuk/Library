from typing import List, TypeVar
from pydantic import BaseModel

from src.core.errors.repository_errors import OBJECT_NOT_FOUND, RESOURCE_ALREADY_EXISTS
from src.core.log_config import logger
from src.core.models.base_model import Base
from src.core.models.user_model import User
from src.core.repository.base_repository import BaseRepository


DB = TypeVar("DB", bound=Base)
P = TypeVar("P", bound=BaseModel)


class BaseService:
    """
    Базовый сервисный класс.

    Attributes:
        repository (BaseRepository): Репозиторий для операций.
    """

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def get_obj_by_id_or_404(self, obj_id: int) -> DB:
        """
        Получение одной записи из базы данных по id.

        Args:
            obj_id (int): id объекта.

        Returns:
            DB: Объект из базы данных.

        Raises:
            404 (not found): Если объект не найден.
        """
        obj_db = await self.repository.get_obj_by_id(obj_id=obj_id)
        if not obj_db:
            raise OBJECT_NOT_FOUND

        return obj_db

    async def get_all_obj(self) -> List[DB]:
        """
        Получает все объекты базы данных.

        Returns:
            List[DB]: Список объектов базы данных.
        """
        return await self.repository.get_all_obj()

    async def create(self, obj_in, user: User = None) -> DB:
        """
        Добвавление нового объекта в базу данных.

        Args:
            obj_in: объект для добавления в базу данных.
            user (User, optional): Пользователь, добавляющий объект.

        Returns:
            DB: Добавленный в базу данных объект.

        Raises:
            409 (conflict): Если объект уже есть в базе данных.
        """
        created_obj = await self.repository.create(obj_in=obj_in)
        if created_obj is False:
            raise RESOURCE_ALREADY_EXISTS

        if user:
            logger.info(f"User with id {user.id} created {created_obj.__class__.__name__} with id {created_obj.id}")

        return created_obj

    async def update(self, obj_in: P, obj_id=None, user: User = None) -> DB:
        """
        Обновление данных.

        Args:
            obj_in (P): Данные для обновления.
            obj_id (int, optional): Идентификатор объекта.
            user (User, optional): Пользователь, обновляющий объект.

        Returns:
            DB: Обновленный объект базы данных.

        Raises:
            404 (not found): Если объект не был найден.
        """
        if not obj_id:
            obj_id = obj_in.id
        obj_db = await self.repository.update(obj_id=obj_id, obj_in=obj_in)
        if obj_db is False:
            raise OBJECT_NOT_FOUND

        if user:
            logger.info(f"User with id {user.id} updated {obj_db.__class__.__name__} with id {obj_db.id}")

        return obj_db

    async def delete(self, obj_id: int, user: User = None) -> None:
        """
        Удаляет объект базы данных.

        Args:
            obj_id (int): Идентификатор объекта.
            user (User, optional): Пользователь, удаляющий объект.

        Returns:
            None

        Raises:
            404 (not found): Если объект не был найден.
        """
        model = await self.repository.delete(obj_id=obj_id)
        if model is False:
            raise OBJECT_NOT_FOUND

        if user:
            logger.info(f"User with id {user.id} deleted {model.__name__} with id {obj_id}")
