from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.db import db
from src.core.repository.fetcher_repository import FetcherRepository
from src.core.schemas.pagination_schema import PaginationParams
from src.core.services.paginated_fetcher import PaginatedFetcher


async def get_paginated_fetcher(
    params: PaginationParams = Depends(), session: AsyncSession = Depends(db.session_getter)
):
    """
    Создание экземпляра PaginatedFetcher с параметрами пагинации и фильтрации.

    Args:
        params (PaginationParams): Параметры пагинации и фильтрации, полученные из запроса FastAPI.
        session (AsyncSession): Сессия SQLAlchemy для работы с базой данных.

    Returns:
        PaginatedFetcher: Экземпляр PaginatedFetcher, готовый для выполнения запросов.
    """
    fetcher_repository = FetcherRepository(session=session)
    return PaginatedFetcher(
        repository=fetcher_repository, offset=params.offset, limit=params.limit, field=params.field, value=params.value
    )
