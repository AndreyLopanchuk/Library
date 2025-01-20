from pydantic import BaseModel, ConfigDict

from src.core.schemas.pagination_schema import Pagination


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str


class PasswordSchema(BaseModel):
    hashed_password: bytes


class UserCreate(UserBase, PasswordSchema):
    pass


class UserDB(UserCreate):
    id: int
    role: str


class UserDBWithoutPassword(UserBase):
    id: int
    role: str


class UserPagination(Pagination):
    data: list[UserDBWithoutPassword]


class RegisteredResponse(BaseModel):
    message: str
    username: str


class UserRegister(UserBase):
    password: str


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
