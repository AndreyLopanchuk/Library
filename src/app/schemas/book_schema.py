from datetime import datetime

from pydantic import BaseModel, conint, ConfigDict

from src.core.schemas.pagination_schema import Pagination


class BookCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    publication_date: datetime
    genres: str
    author_id: int
    available: conint(ge=0)


class BookUpdate(BookCreate):
    id: int


class BookDB(BookUpdate):
    pass


class BookPagination(Pagination):
    data: list[BookDB]
