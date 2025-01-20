from fastapi import HTTPException, status


NO_COPIES = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="There are no copies of the book available",
)

BOOK_BEEN_RETURNED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The book has already been returned",
)

BORROW_LIMIT_EXCEEDED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="You can't borrow more than 5 books at the same time",
)
