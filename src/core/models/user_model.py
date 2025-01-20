import enum

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base_model import Base


class PermissionsEnum(str, enum.Enum):
    READER = "reader"
    ADMIN = "admin"


class User(Base):
    """
    Модель пользователя.

    Attributes:
        username (str): Логин пользователя.
        hashed_password (bytes): Хэш пароля пользователя.
        role (PermissionsEnum): Роль пользователя.
    """

    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[bytes] = mapped_column(BYTEA, nullable=False)
    role: Mapped[PermissionsEnum] = mapped_column(default=PermissionsEnum.READER, server_default=text("'READER'"))
