from fastapi import APIRouter, Depends, status

from src.app.api.borrows.borrow_dependencies import get_borrow_service, get_borrow_service_with_book
from src.app.models.borrow_model import Borrow
from src.app.schemas.borrow_schema import BorrowDB, BorrowPagination
from src.app.services.borrow_service import BorrowService
from src.auth.api.auth_dependencies import has_reader_permissions, has_admin_permissions
from src.core.dependencies.fetcher_dependencies import get_paginated_fetcher
from src.core.models.user_model import User
from src.core.services.paginated_fetcher import PaginatedFetcher

router = APIRouter(prefix="/borrows", tags=["API для управления выдачами книг."])


@router.post(
    "/",
    summary="Создание записи о выдаче книги",
    response_model=BorrowDB,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_borrow_endpoint(
    book_id: int,
    borrow_service: BorrowService = Depends(get_borrow_service_with_book),
    user: User = Depends(has_reader_permissions),
):
    """
    ### Создание записи о выдаче книги
    ----------------

    * **POST /borrows/**
    + **Description**: Создает новую запись о выдаче книги.
    + **Request**: **BorrowCreate**
    + **Response**: **BorrowDB**
    + **Status Code**: 201 Created
    + **Errors**:
        - **400 (Bad Request):** Превышен лимит выдач книг.
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **404 (Not Found):** Книга не найдена.
        - **409 (Conflict):** Нет свободных экземпляров книги.
    """
    return await borrow_service.create_borrow(book_id=book_id, user=user)


@router.get(
    "/user-borrows/",
    summary="Получение списка всех выдач книг пользователя",
    response_model=BorrowPagination,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_borrows_endpoint(
    paginated_fetcher: PaginatedFetcher = Depends(get_paginated_fetcher),
    user: User = Depends(has_reader_permissions),
):
    """
    ### Получение всех выдач книг
    ----------------------

    * **GET /borrows/user-borrows/**
    + **Description**: Возвращает список всех выдач книг пользователя из базы данных с пагинацией и фильтрацией.
    + **Parameters**:
        - **limit** (int) - Количество объектов для пагинации.
        - **offset** (int) - Начальный индекс для пагинации.
        - **field** (str, optional) - Поле для фильтрации.
        - **value** (Any, optional) - Значение для фильтрации.
    + **Response**: **BorrowPagination** (List[BorrowDB])
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
    """
    return await paginated_fetcher.fetch_by_reader_id(model=Borrow, reader_id=user.id)


@router.get(
    "/",
    summary="Получение списка всех выдач книг",
    response_model=BorrowPagination,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_borrows_endpoint(
    paginated_fetcher: PaginatedFetcher = Depends(get_paginated_fetcher),
    user: User = Depends(has_admin_permissions),
):
    """
    ### Получение всех выдач книг
    ----------------------

    * **GET /borrows/**
    + **Description**: Возвращает список всех выдач книг из базы данных с пагинацией и фильтрацией.
    + **Parameters**:
        - **limit** (int) - Количество объектов для пагинации.
        - **offset** (int) - Начальный индекс для пагинации.
        - **field** (str, optional) - Поле для фильтрации.
        - **value** (Any, optional) - Значение для фильтрации.
    + **Response**: **BorrowPagination** (List[BorrowDB])
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **403 (Forbidden):** Пользователь не имеет прав администратора.
    """
    return await paginated_fetcher.get_paginated_list(model=Borrow)


@router.get(
    "/{borrow_id}/",
    summary="Получение информации о выдаче книги",
    response_model=BorrowDB,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_borrow_endpoint(
    borrow_id: int,
    borrow_service: BorrowService = Depends(get_borrow_service),
    user: User = Depends(has_admin_permissions),
):
    """
    ### Получение информации о выдаче книги
    -----------------------------

    * **GET /borrows/{borrow_id}**
    + **Description**: Возвращает информацию о выдаче книги по входящему ID.
    + **Parameters**:
        - **borrow_id** (int): ID выдачи книги, которую нужно получить.
    + **Response**: **BorrowDB**
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **403 (Forbidden):** Пользователь не имеет прав администратора.
        - **404 (Not Found)**: Выдача книги с указанным ID не найдена.
    """
    return await borrow_service.get_obj_by_id_or_404(obj_id=borrow_id)


@router.patch(
    "/{borrow_id}/return/",
    summary="Завершение выдачи книги",
    response_model=BorrowDB,
    status_code=status.HTTP_200_OK,
)
async def borrow_completion_endpoint(
    borrow_id: int,
    borrow_service: BorrowService = Depends(get_borrow_service_with_book),
    user: User = Depends(has_reader_permissions),
):
    """
    ### Завершение выдачи книги
    ------------------------------

    * **PATCH /borrows/{borrow_id}/return**
    + **Description**: Завершает выдачу книги по входящему ID, устанавливает время сдачи.
    + **Parameters**:
        - **borrow_id** (int): ID выдачи книги, которую нужно завершить.
    + **Response**: **BorrowDB**
    + **Status Code**: 200 OK
    + **Errors**:
        - **400 (Bad Request):** Книга уже возвращена.
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **404 (Not Found)**: Выдача книги с указанным ID не найдена.
    """
    return await borrow_service.close_borrow(borrow_id, user=user)
