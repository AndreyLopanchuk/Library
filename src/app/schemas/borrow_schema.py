from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.core.schemas.pagination_schema import Pagination


class BorrowCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: int
    reader_id: int


class BorrowUpdate(BorrowCreate):
    id: int
    borrow_date: datetime


class BorrowClose(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    return_date: datetime


class BorrowDB(BorrowUpdate):
    return_date: datetime | None


class BorrowPagination(Pagination):
    data: list[BorrowDB]
