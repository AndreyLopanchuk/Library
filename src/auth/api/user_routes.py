from fastapi import Depends, Response, APIRouter, Form

from src.auth.api import http_bearer
from src.auth.api.auth_dependencies import get_auth_service, has_reader_permissions, has_admin_permissions
from src.auth.schemas.token_schema import TokenSchema
from src.auth.services.auth_service import AuthService
from src.auth.utils import set_auth_tokens
from src.core.dependencies.fetcher_dependencies import get_paginated_fetcher
from src.core.models.user_model import User
from src.core.schemas.user_schema import UserBase, UserPagination, UserChangePassword
from src.core.services.paginated_fetcher import PaginatedFetcher

router = APIRouter(
    prefix="/users", tags=["API для управления личными данными пользователя."], dependencies=[Depends(http_bearer)]
)


@router.patch(
    "/update-password/",
    summary="Смена пароля",
    status_code=200,
    response_model=TokenSchema,
)
async def update_password(
    response: Response,
    credentials: UserChangePassword = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
    user: User = Depends(has_reader_permissions),
):
    """
    ### Смена пароля
    ----------------

    * **PATCH /users/update-password/**
    + **Description**: Смена пароля пользователя.
    + **Request**: **UserChangePassword**
    + **Response**: **TokenSchema**
    + **Status Code**: 200 OK
    + **Errors**:
        - **400 (Bad Request):** Новый пароль и подтверждающий пароль не совпадают.
        - **401 (Unauthorized):** Неправильный старый пароль.
        - **401 (Unauthorized):** Пользователь не авторизован.
    """
    await auth_service.update_password(user=user, credentials=credentials)
    tokens = await auth_service.issue_tokens(user=user)

    return set_auth_tokens(response, tokens)


@router.patch(
    "/update-info/",
    summary="Обновление личной информации пользователя",
    status_code=200,
    response_model=UserBase,
)
async def user_update(
    user_in: UserBase,
    auth_service: AuthService = Depends(get_auth_service),
    user: User = Depends(has_reader_permissions),
):
    """
    ### Обновление личной информации пользователя
    ----------------

    * **PATCH /users/update-info/**
    + **Description**: Обновление личной информации пользователя.
    + **Request**: **UserBase**
    + **Response**: **UserBase**
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
    """
    return await auth_service.update_user_info(user=user, user_in=user_in)


@router.get(
    "/users-list/",
    summary="Просмотр списка пользователей",
    status_code=200,
    response_model=UserPagination,
)
async def users_list(
    paginated_fetcher: PaginatedFetcher = Depends(get_paginated_fetcher),
    user: User = Depends(has_admin_permissions),
):
    """
    ### Просмотр списка пользователей
    ----------------------

    * **GET /users/users-list/**
    + **Description**: Возвращает список всех пользователей из базы данных с пагинацией и фильтрацией.
    + **Parameters**:
        - **limit** (int) - Количество объектов для пагинации.
        - **offset** (int) - Начальный индекс для пагинации.
        - **field** (str, optional) - Поле для фильтрации.
        - **value** (Any, optional) - Значение для фильтрации.
    + **Response**: **UserPagination** (List[UserDB])
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Пользователь не авторизован.
        - **403 (Forbidden):** Пользователь не имеет прав администратора.
    """
    return await paginated_fetcher.get_paginated_list(User)
