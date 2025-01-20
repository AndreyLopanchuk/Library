from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base_model import Base
from src.core.models.user_model import User

if TYPE_CHECKING:
    from src.app.models.book_model import Book


class Borrow(Base):
    """
    Модель выдачи книг.

    Attributes:
        borrow_date (datetime): Дата взятия книги.
        return_date (datetime | None): Дата возврата книги.
        book_id (int): Идентификатор книги.
        reader_id (int): Идентификатор читателя.

        book (Book): Книга, связанная с выдачей.
        reader (User): Читатель, связанный с выдачей.
    """

    borrow_date: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    return_date: Mapped[datetime | None]

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    reader_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    book: Mapped["Book"] = relationship("Book", back_populates="borrows")
    reader: Mapped["User"] = relationship("User", backref="books")
