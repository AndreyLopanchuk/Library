from typing import TYPE_CHECKING

from sqlalchemy import Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base_model import Base

if TYPE_CHECKING:
    from src.app.models.book_model import Book


class Author(Base):
    """
    Модель автора.

    Attributes:
        name (str): Имя автора.
        biography (str): Биография.
        birth_date (Date): Дата рождения автора.

        books (list[Book]): Книги, связанные с автором.
    """

    name: Mapped[str]
    biography: Mapped[str]
    birth_date: Mapped[Date] = mapped_column(Date)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("name", "birth_date"),)
