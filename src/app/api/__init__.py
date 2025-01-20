from fastapi import APIRouter

from src.app.api.authors.author_routes import router as authors_router
from src.app.api.books.book_routes import router as books_router
from src.app.api.borrows.borrow_routes import router as borrows_router

app_router = APIRouter()

app_router.include_router(authors_router)
app_router.include_router(books_router)
app_router.include_router(borrows_router)
