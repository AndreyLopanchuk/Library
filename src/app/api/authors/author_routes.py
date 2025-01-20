from fastapi import APIRouter, Depends, status

from src.app.api.authors.author_dependencies import get_author_service
from src.app.models.author_model import Author
from src.app.schemas.author_schema import AuthorCreate, AuthorUpdate, AuthorPagination, AuthorDB
from src.app.services.author_service import AuthorService

from src.auth.api.auth_dependencies import has_reader_permissions, has_admin_permissions
from src.core.dependencies.fetcher_dependencies import get_paginated_fetcher
from src.core.models.user_model import User
from src.core.services.paginated_fetcher import PaginatedFetcher

router = APIRouter(prefix="/authors", tags=["API для управления авторами."])


@router.post(
    "/",
    summary="Создание автора",
    response_model=AuthorDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_author_endpoint(
    author_in: AuthorCreate,
    author_service: AuthorService = Depends(get_author_service),
    user: User = Depends(has_admin_permissions),
):
    """
    ### Добавление автора
    ----------------

    * **POST /authors/**
    + **Description**: Добавляет нового автора в базу данных.
    + **Request**: **AuthorCreate**
    + **Response**: **AuthorDB**
    + **Status Code**: 201 Created
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **403 (Forbidden):** Пользователь не имеет права добавлять автора.
        - **409 (Conflict):** Автор с таким именем и датой рождения уже существует.
    """
    return await author_service.create(obj_in=author_in, user=user)


@router.get(
    "/",
    summary="Получение всех авторов",
    response_model=AuthorPagination,
    status_code=status.HTTP_200_OK,
)
async def get_authors_endpoint(
    paginated_fetcher: PaginatedFetcher = Depends(get_paginated_fetcher),
    user: User = Depends(has_reader_permissions),
):
    """
    ### Получение всех авторов
    ----------------------

    * **GET /authors/**
    + **Description**: Возвращает список всех авторов из базы данных с пагинацией и фильтрацией.
    + **Parameters**:
        - **limit** (int) - Количество объектов для пагинации.
        - **offset** (int) - Начальный индекс для пагинации.
        - **field** (str, optional) - Поле для фильтрации.
        - **value** (Any, optional) - Значение для фильтрации.
    + **Response**: **AuthorPagination** (List[AuthorDB])
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
    """
    return await paginated_fetcher.get_paginated_list(model=Author)


@router.get(
    "/{author_id}/",
    summary="Получение информации об авторе",
    response_model=AuthorDB,
    status_code=status.HTTP_200_OK,
)
async def get_author_endpoint(
    author_id: int,
    author_service: AuthorService = Depends(get_author_service),
    user: User = Depends(has_reader_permissions),
):
    """
    ### Получение информации об авторе
    -----------------------------

    * **GET /authors/{author_id}**
    + **Description**: Возвращает информацию об авторе по входящему ID.
    + **Parameters**:
        - **author_id** (int) - ID автора
    + **Response**: **AuthorDB**
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **404 (Not Found)**: Автор с указанным ID не найден.
    """
    return await author_service.get_obj_by_id_or_404(obj_id=author_id)


@router.put(
    "/{author_id}/",
    summary="Обновление информации об авторе",
    response_model=AuthorDB,
    status_code=status.HTTP_200_OK,
)
async def update_author_endpoint(
    author_in: AuthorUpdate,
    author_service: AuthorService = Depends(get_author_service),
    user: User = Depends(has_admin_permissions),
):
    """
    ### Обновление информации об авторе
    ------------------------------

    * **PUT /authors/{author_id}**
    + **Description**: Обновляет информацию об авторе по ID.
    + **Request**: **AuthorUpdate**
    + **Response**: **AuthorDB**
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **403 (Forbidden):** Пользователь не имеет права обновлять автора.
        - **404 (Not Found)**: Автор с указанным ID не найден.
    """
    return await author_service.update(obj_in=author_in, user=user)


@router.delete(
    "/{author_id}/",
    summary="Удаление автора",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_author_endpoint(
    author_id: int,
    author_service: AuthorService = Depends(get_author_service),
    user: User = Depends(has_admin_permissions),
):
    """
     ### Удаление автора
    ----------------

    * **DELETE /authors/{author_id}**
    + **Description**: Удаляет автора по ID.
    + **Parameters**:
        - **author_id** (int) - ID автора для удаления.
    + **Status Code**: 204 No Content
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **403 (Forbidden):** Пользователь не имеет права удалять автора.
        - **404 (Not Found)**: Автор с указанным ID не найден.
    """
    await author_service.delete(obj_id=author_id, user=user)
