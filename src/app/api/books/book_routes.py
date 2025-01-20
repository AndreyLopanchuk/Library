from fastapi import APIRouter, Depends, status

from src.app.api.books.book_dependencies import get_book_service, get_book_service_with_author
from src.app.models.book_model import Book
from src.app.schemas.book_schema import BookCreate, BookUpdate, BookPagination, BookDB
from src.app.services.book_service import BookService
from src.auth.api.auth_dependencies import has_reader_permissions, has_admin_permissions
from src.core.dependencies.fetcher_dependencies import get_paginated_fetcher
from src.core.models.user_model import User
from src.core.services.paginated_fetcher import PaginatedFetcher

router = APIRouter(prefix="/books", tags=["API для управления книгами."])


@router.post(
    "/",
    summary="Добавление книги",
    response_model=BookDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_book_endpoint(
    book_in: BookCreate,
    book_service: BookService = Depends(get_book_service_with_author),
    user: User = Depends(has_admin_permissions),
):
    """
    ### Добавление книги
    ----------------

    * **POST /books/**
    + **Description**: Добавляет новую книгу в базу данных.
    + **Request**: **BookCreate**
    + **Response**: **BookDB**
    + **Status Code**: 201 Created
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **403 (Forbidden):** Пользователь не имеет права добавлять книгу.
        - **409 (Conflict):** Книга с таким названием и автором уже существует.
    """
    return await book_service.create(book_in=book_in, user=user)


@router.get(
    "/",
    summary="Получение списка книг",
    response_model=BookPagination,
    status_code=status.HTTP_200_OK,
)
async def get_books_endpoint(
    paginated_fetcher: PaginatedFetcher = Depends(get_paginated_fetcher),
    user: User = Depends(has_reader_permissions),
):
    """
    ### Получение всех книг
    ----------------------

    * **GET /books/**
    + **Description**: Возвращает список всех книг из базы данных с пагинацией и фильтрацией.
    + **Parameters**:
        - **limit** (int) - Количество объектов для пагинации.
        - **offset** (int) - Начальный индекс для пагинации.
        - **field** (str, optional) - Поле для фильтрации.
        - **value** (Any, optional) - Значение для фильтрации.
    + **Response**: **BookPagination**: (List[BookDB])
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
    """
    return await paginated_fetcher.get_paginated_list(model=Book)


@router.get(
    "/{book_id}/",
    summary="Получение информации о книге",
    response_model=BookDB,
    status_code=status.HTTP_200_OK,
)
async def get_book_endpoint(
    book_id: int,
    book_service: BookService = Depends(get_book_service),
    user: User = Depends(has_reader_permissions),
):
    """
    ### Получение информации о книге
    -----------------------------

    * **GET /books/{book_id}**
    + **Description**: Возвращает информацию о книге по входящему ID.
    + **Parameters**:
        - **book_id** (int) - Идентификатор книги
    + **Response**: **BookDB**
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **404 (Not Found)**: Книга с указанным ID не найдена.
    """
    return await book_service.get_obj_by_id_or_404(obj_id=book_id)


@router.put(
    "/{book_id}/",
    summary="Обновление информации о книге",
    response_model=BookDB,
    status_code=status.HTTP_200_OK,
)
async def update_book_endpoint(
    book_in: BookUpdate,
    book_service: BookService = Depends(get_book_service_with_author),
    user: User = Depends(has_admin_permissions),
):
    """
    ### Обновление информации о книге
    ------------------------------

    * **PUT /books/{book_id}**
    + **Description**: Обновляет информацию о книге по входящему ID.
    + **Request**: **BookUpdate**
    + **Response**: **BookDB**
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **403 (Forbidden):** Пользователь не имеет права обновлять книгу.
        - **404 (Not Found)**: Книга с указанным ID не найдена.
    """
    return await book_service.update(book_in=book_in, user=user)


@router.delete(
    "/{book_id}/",
    summary="Удаление книги",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book_endpoint(
    book_id: int,
    book_service: BookService = Depends(get_book_service),
    user: User = Depends(has_admin_permissions),
):
    """
    ### Удаление книги
    ----------------

    * **DELETE /books/{book_id}**
    + **Description**: Удаляет книгу по ее ID.
    + **Parameters**:
        - **book_id** (int) - Идентификатор удаляемой книги
    + **Status Code**: 204 No Content
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **403 (Forbidden):** Пользователь не имеет права удалять книгу.
        - **404 (Not Found)**: Книга с указанным ID не найдена.
    """
    await book_service.delete(obj_id=book_id, user=user)
