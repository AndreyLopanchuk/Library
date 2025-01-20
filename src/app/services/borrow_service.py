from datetime import datetime

from src.app.models.borrow_model import Borrow
from src.app.repository.borrow_repository import BorrowRepository
from src.app.schemas.borrow_schema import BorrowCreate, BorrowClose
from src.core.errors.repository_errors import OBJECT_NOT_FOUND
from src.core.errors.service_errors import NO_COPIES, BOOK_BEEN_RETURNED, BORROW_LIMIT_EXCEEDED
from src.core.models.user_model import User
from src.core.services.base_service import BaseService
from src.app.services.book_service import BookService


class BorrowService(BaseService):
    """
    Сервисный класс для управления выдачами книг.

    Attributes:
        repository (BorrowRepository): Репозиторий для операций с выдачами книг.
        book_service (BookService, optional): Сервис для работы с книгами.
    """

    def __init__(self, borrow_repository: BorrowRepository, book_service: BookService = None):
        super().__init__(repository=borrow_repository)
        self.book_service = book_service
        self.repository = borrow_repository

    async def create_borrow(self, book_id: int, user: User = None) -> Borrow:
        """
        Создает новую выдачу.

        Args:
            book_id (int): Идентификатор книги.
            user (User, optional): Пользователь, который получает книгу.

        Returns:
            Borrow: Созданный объект выдачи.

        Raises:
            400 (Bad request): Если книга не была найдена.
            404 (Not found): Если книга не была найдена.
            409 (Сonflict): Если нет доступных экземпляров книги.
        """
        borrow_count = await self.repository.get_borrows_count(reader_id=user.id)
        if borrow_count >= 5:
            raise BORROW_LIMIT_EXCEEDED

        borrow_in = BorrowCreate(book_id=book_id, reader_id=user.id)
        result = await self.book_service.update_book_available(book_id=book_id, delta=-1)
        if result is False:
            raise NO_COPIES

        if result is None:
            raise OBJECT_NOT_FOUND

        return await super().create(obj_in=borrow_in, user=user)

    async def close_borrow(self, borrow_id: int, user: User = None) -> Borrow:
        """
        Закрывает выдачу.

        Args:
            borrow_id (int): Идентификатор выдачи.
            user (User, optional): Пользователь, закрывающий выдачу.

        Returns:
            Borrow: Обновленный объект выдачи.

        Raises:
            400 (Bad request): Если книга уже возвращена.
        """
        borrow_db = await super().get_obj_by_id_or_404(obj_id=borrow_id)
        returned_book = await self.book_service.get_obj_by_id_or_404(obj_id=borrow_db.book_id)
        if borrow_db.return_date:
            raise BOOK_BEEN_RETURNED

        await self.book_service.update_book_available(book_id=returned_book.id, delta=1)
        borrow_return = BorrowClose(return_date=datetime.now(), id=borrow_id)

        return await super().update(obj_in=borrow_return, user=user)
