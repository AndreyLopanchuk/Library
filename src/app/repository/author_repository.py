from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.author_model import Author
from src.core.repository.base_repository import BaseRepository


class AuthorRepository(BaseRepository):
    """
    Репозиторий для операций с авторами.

    Attributes:
        session (AsyncSession): Асинхронная сессия базы данных.
        model (Author): Модель данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Author)
