from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, Date, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base_model import Base


if TYPE_CHECKING:
    from src.app.models.author_model import Author
    from src.app.models.borrow_model import Borrow


class Book(Base):
    """
    Модель книги.

    Attributes:
        title (str): Название книги.
        description (str): Описание книги.
        publication_date (Date): Дата публикации книги.
        genres (str): Жанры книги.
        author_id (int): Идентификатор автора книги.
        available (int): Количество доступных экземпляров книги.

        author (Author): Автор, связанный с книгой.
        borrows (list[Borrow]): Выдачи, связанные с книгой.
    """

    title: Mapped[str]
    description: Mapped[str]
    genres: Mapped[str]
    publication_date: Mapped[Date] = mapped_column(Date)
    available: Mapped[int] = mapped_column(CheckConstraint("available >= 0"))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="book", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("title", "author_id"),)
