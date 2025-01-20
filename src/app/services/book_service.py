from src.app.models.book_model import Book
from src.app.repository.book_repository import BookRepository
from src.app.schemas.book_schema import BookCreate, BookUpdate
from src.app.services.author_service import AuthorService
from src.core.models.user_model import User
from src.core.services.base_service import BaseService


class BookService(BaseService):
    """
    Сервис для работы с книгами.

    Attributes:
        repository (BookRepository): Репозиторий для работы с книгами.
    """

    def __init__(self, book_repository: BookRepository, author_service: AuthorService = None):
        super().__init__(repository=book_repository)
        self.author_service = author_service
        self.repository = book_repository

    async def create(self, book_in: BookCreate, user: User = None) -> Book:
        """
        Добвавление новой книги.

        Args:
            book_in (BookCreate): Данные для новой книги.
            user (User, optional): Пользователь, добавляющий книгу.

        Returns:
            Book: Модель добавленной книги.

        Raises:
            404 (not found): Если автора нет в базе данных.
            409 (conflict): Если книга уже есть в базе данных.
        """
        await self.author_service.get_obj_by_id_or_404(obj_id=book_in.author_id)

        return await super().create(obj_in=book_in, user=user)

    async def update(self, book_in: BookUpdate, obj_id: int = None, user: User = None) -> Book:
        """
        Обновление данных книги.

        Args:
            obj_id (int, optional): Идентификатор книги.
            book_in (BookCreate): Данные для обновления книги.
            user (User, optional): Пользователь, обновляющий книгу.

        Returns:
            Book: Модель обновлённой книги.

        Raises:
            404 (not found): Если автора нет в базе данных.
            404 (not found): Если книга не была найдена.
        """
        await self.author_service.get_obj_by_id_or_404(obj_id=book_in.author_id)

        return await super().update(obj_in=book_in, user=user)

    async def update_book_available(self, book_id: int, delta: int) -> bool | None:
        """
        Обновление количеста доступных экземпляров книги.

        Args:
            book_id (int): Идентификатор книги.
            delta (int): Изменение количеста доступных экземпляров книги.

        Returns:
            None: Eсли книга не была найдена.
            True: Количество доступных книг успешно обновлено.
            False: Если произошла ошибка обновления.

        Raises:
            404 (not found): Если книга не была найдена.
        """
        return await self.repository.update_available(book_id=book_id, delta=delta)
