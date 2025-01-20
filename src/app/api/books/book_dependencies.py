from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.authors.author_dependencies import get_author_service
from src.app.repository.book_repository import BookRepository
from src.core.database.db import db
from src.app.services.book_service import BookService


async def get_book_service(session: AsyncSession = Depends(db.session_getter)) -> BookService:
    """
    Получение сервиса для работы с книгами

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        BookService: Сервис для работы с книгами.
    """
    book_repository = BookRepository(session=session)
    return BookService(book_repository=book_repository)


async def get_book_service_with_author(session: AsyncSession = Depends(db.session_getter)) -> BookService:
    """
    Получение сервиса для работы с книгами с внедрённой зависимостью, сервисом авторов

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        BookService: Сервис для работы с книгами.
    """
    book_repository = BookRepository(session=session)
    author_service = await get_author_service(session=session)
    return BookService(book_repository=book_repository, author_service=author_service)
