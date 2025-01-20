from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.book_model import Book
from src.core.repository.base_repository import BaseRepository


class BookRepository(BaseRepository):
    """
    Репозиторий для операций с книгами.

    Attributes:
        session (AsyncSession): Асинхронная сессия базы данных.
        model (Book): Модель данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Book)
        self.session = session

    async def update_available(self, book_id: int, delta: int) -> bool | None:
        """
        Обновляет количество доступных книг.

        Args:
            book_id (int): Идентификатор книги.
            delta (int): Изменение количества доступных книг.

        Returns:
            None: Eсли книга не была найдена.
            True: Количество доступных книг успешно обновлено.
            False: Если произошла ошибка обновления.
        """
        try:
            stmt = update(Book).where(Book.id == book_id).values(available=Book.available + delta)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                return None

            return True

        except IntegrityError:
            return False
