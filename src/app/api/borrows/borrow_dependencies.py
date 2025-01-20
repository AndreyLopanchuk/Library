from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.books.book_dependencies import get_book_service
from src.app.repository.borrow_repository import BorrowRepository
from src.core.database.db import db
from src.app.services.borrow_service import BorrowService


async def get_borrow_service(session: AsyncSession = Depends(db.session_getter)) -> BorrowService:
    """
    Получение сервиса для работы с выдачами книг

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        BorrowService: Сервис для работы с выдачами книг.
    """
    borrow_repository = BorrowRepository(session=session)
    return BorrowService(borrow_repository=borrow_repository)


async def get_borrow_service_with_book(session: AsyncSession = Depends(db.session_getter)) -> BorrowService:
    """
    Получение сервиса для работы с выдачами книг с внедрённой зависимостью, сервисом для работы с книгами

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        BorrowService: Сервис для работы с выдачами книг.
    """
    borrow_repository = BorrowRepository(session=session)
    book_service = await get_book_service(session=session)
    return BorrowService(borrow_repository=borrow_repository, book_service=book_service)
