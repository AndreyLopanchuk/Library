from fastapi import APIRouter, Depends, Cookie, Form
from fastapi import Response
from fastapi.security import HTTPBearer

from src.auth.api.auth_dependencies import get_auth_service
from src.auth.schemas.token_schema import TokenSchema
from src.auth.services.auth_service import AuthService
from src.core.schemas.user_schema import RegisteredResponse, UserRegister
from src.auth.utils import set_auth_tokens


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/auth", tags=["API управления доступом"])


@router.post(
    "/register/",
    summary="Регистрация нового пользователя",
    status_code=201,
    response_model=RegisteredResponse,
)
async def register_user_endpoint(
    form_data: UserRegister = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    ### Регистрация нового пользователя
    ----------------

    * **POST /auth/register/**
    + **Description**: Добавляет нового пользователя в базу данных.
    + **Request**: **UserRegister**
    + **Response**: **RegisteredResponse**
    + **Status Code**: 201 Created
    + **Errors**:
        - **409 (Conflict):** Пользователь с таким именем уже существует.
    """
    user = await auth_service.create_user(form_data=form_data)

    return {"message": "Registration is completed", "username": user.username}


@router.post(
    "/token/",
    summary="Выдача access и refresh токенов по логину и паролю",
    status_code=200,
    response_model=TokenSchema,
)
async def login(
    response: Response,
    form_data: UserRegister = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    ### Выдача access и refresh токенов по логину и паролю
    ----------------

    * **POST /auth/token/**
    + **Description**: Выдача access и refresh токенов по логину и паролю.
    + **Request**: **UserRegister**
    + **Response**: **TokenSchema**
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Неправильный логин или пароль.
    """
    tokens = await auth_service.issue_tokens_by_password(form_data=form_data)

    return set_auth_tokens(response, tokens)


@router.post(
    "/refresh/",
    summary="Выдача access и refresh токенов по refresh",
    status_code=200,
    response_model=TokenSchema,
)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    ### Выдача access и refresh токенов по refresh
    ----------------

    * **POST /auth/refresh/**
    + **Description**: Выдача access и refresh токенов по refresh токену.
    + **Response**: **TokenSchema**
    + **Status Code**: 200 OK
    + **Errors**:
        - **401 (Unauthorized):** Отсутствует в cookie или невалидный refresh токен.
    """
    tokens = await auth_service.reissue_tokens_by_refresh(refresh_token=refresh_token)

    return set_auth_tokens(response, tokens)
