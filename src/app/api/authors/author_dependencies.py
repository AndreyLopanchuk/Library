from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repository.author_repository import AuthorRepository
from src.core.database.db import db
from src.app.services.author_service import AuthorService


async def get_author_service(session: AsyncSession = Depends(db.session_getter)) -> AuthorService:
    """
    Получение сервиса для работы с авторами.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        AuthorService: Экземпляр сервиса для работы с авторами.
    """
    author_repository = AuthorRepository(session=session)
    return AuthorService(author_repository=author_repository)
