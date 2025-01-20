from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository.auth_repository import AuthRepository
from src.auth.repository.token_repository import TokenRepository, get_token_repository
from src.auth.services.auth_service import AuthService
from src.auth.services.password_service import PasswordManager, get_password_manager
from src.auth.services.token_service import JWTokenManager, get_token_service
from src.core.database.db import db
from src.core.models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=True)


async def get_auth_repository(session: AsyncSession = Depends(db.session_getter)) -> AuthRepository:
    """
    Получение репозитория управления доступом.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
    """
    return AuthRepository(session=session)


async def get_auth_service(
    token_service: JWTokenManager = Depends(get_token_service),
    token_repository: TokenRepository = Depends(get_token_repository),
    passwords_manager: PasswordManager = Depends(get_password_manager),
    auth_repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    """
    Получение сервиса управления доступом с внедрёнными в него зависимостями, сервисами управления токенами и паролями.

    Args:
        token_service (JWTokenManager): Сервис управления токенами.
        token_repository (TokenRepository): Репозиторий управления токенами.
        passwords_manager (PasswordManager): Сервис управления паролями.
        auth_repository (AuthRepository): Репозиторий управления пользователями.

    Returns:
        AuthService: Сервис управления доступом.
    """
    return AuthService(
        token_repository=token_repository,
        passwords_manager=passwords_manager,
        token_service=token_service,
        auth_repository=auth_repository,
    )


async def has_admin_permissions(
    auth_service: AuthService = Depends(get_auth_service), access_token: str = Depends(oauth2_scheme)
) -> User:
    """Проверка действительности access токена и ограничение доступа к ресурсам по роли"""
    return await auth_service.has_permissions(access_token=access_token, permissions=["admin"])


async def has_reader_permissions(
    auth_service: AuthService = Depends(get_auth_service), access_token: str = Depends(oauth2_scheme)
) -> User:
    """Проверка действительности access токена и ограничение доступа к ресурсам по роли"""
    return await auth_service.has_permissions(access_token=access_token, permissions=["admin", "reader"])
