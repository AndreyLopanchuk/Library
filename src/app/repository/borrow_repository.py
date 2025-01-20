from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.borrow_model import Borrow
from src.core.repository.base_repository import BaseRepository


class BorrowRepository(BaseRepository):
    """
    Репозиторий для операций с выдачами книг.

    Attributes:
        session (AsyncSession): Асинхронная сессия базы данных.
        model (Borrow): Модель данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Borrow)
        self.session = session

    async def get_borrows_count(self, reader_id: int) -> int:
        """
        Возвращает количество выданных пользователю книг.

        Args:
            reader_id (int): Идентификатор пользователя.

        Returns:
            int: Колтчество выданных пользователю книг.
        """
        filter_dict = {"reader_id": reader_id, "return_date": None}
        stmt = select(func.count(self.model.id)).filter_by(**filter_dict)

        return await self.session.scalar(stmt)
