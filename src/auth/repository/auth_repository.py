from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.user_model import User
from src.core.repository.base_repository import BaseRepository


class AuthRepository(BaseRepository):
    """
    Репозиторий для операций с управлением доступом.

    Attributes:
        session (AsyncSession): Асинхронная сессия базы данных.
        model (User): Модель данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)

    async def get_one_by_field(self, value: Any, field: str) -> User | None:
        """
        Получение одной записи из базы данных по полю.

        Args:
            value (Any): значение поля.
            field (str): название поля.

        Returns:
            DB: Объект из базы данных.
            None: Если объект не найден.
        """
        if field and hasattr(self.model, field):
            filter_dict = {field: value}
            stmt = select(self.model).filter_by(**filter_dict)
            result = await self.session.scalars(stmt)

            return result.first()
