from typing import Any

from pydantic import BaseModel, conint, ConfigDict


class Pagination(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    offset: int
    limit: int
    totalCount: int


class PaginationParams(BaseModel):
    offset: conint(ge=0)
    limit: conint(ge=0)
    field: str | None = None
    value: Any | None = None
