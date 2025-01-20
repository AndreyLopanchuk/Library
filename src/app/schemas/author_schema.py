from datetime import date

from pydantic import BaseModel, ConfigDict

from src.core.schemas.pagination_schema import Pagination


class AuthorCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    biography: str
    birth_date: date


class AuthorUpdate(AuthorCreate):
    id: int


class AuthorDB(AuthorUpdate):
    pass


class AuthorPagination(Pagination):
    data: list[AuthorDB]
