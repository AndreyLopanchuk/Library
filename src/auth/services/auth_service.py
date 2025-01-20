from src.core.errors.auth_errors import (
    FORBIDDEN,
    INVALID_AUTHENTICATION_CREDENTIALS,
    INVALID_ACCESS_TOKEN,
    INVALID_REFRESH_TOKEN,
    PASSWORDS_MISMATCH,
)
from src.auth.repository.token_repository import TokenRepository
from src.auth.services.password_service import PasswordManager
from src.core.models.user_model import User
from src.core.schemas.user_schema import UserCreate, UserBase, UserChangePassword, PasswordSchema, UserRegister
from src.auth.services.token_service import JWTokenManager
from src.core.config import settings
from src.core.services.base_service import BaseService
from src.auth.repository.auth_repository import AuthRepository


class AuthService(BaseService):
    """
    Сервисный класс для управления доступом.

    Attributes:
        repository (AuthRepository): Репозиторий для работы с управления доступом.
        passwords_manager (PasswordManager): Сервис управления паролями.
        token_repository (TokenRepository): Репозиторий управления токенами.
        token_service (JWTokenManager): Сервис управления токенами.
    """

    def __init__(
        self,
        auth_repository: AuthRepository,
        passwords_manager: PasswordManager,
        token_repository: TokenRepository,
        token_service: JWTokenManager,
    ):
        super().__init__(repository=auth_repository)
        self.passwords_manager = passwords_manager
        self.token_repository = token_repository
        self.token_service = token_service
        self.repository = auth_repository

    async def create_user(self, form_data: UserRegister) -> User:
        """
        Добавление нового пользователя в базу данных

        Args:
            form_data (UserRegister): Данные о новом пользователе

        Returns:
            User: Добавленный пользователь

        Raises:
            409 (conflict): Если пользователь с таким логином уже есть в базе данных
        """
        user_create = UserCreate(
            username=form_data.username,
            hashed_password=self.passwords_manager.hash_password(form_data.password),
        )

        return await super().create(obj_in=user_create)

    async def update_user_info(self, user: User, user_in: UserBase) -> User:
        """
        Обновление личной информации пользователя

        Args:
            user (User): Пользователь, которого нужно обновить
            user_in (UserBase): Данные о пользователе, которые нужно обновить

        Returns:
            User: Обновленный пользователь
        """
        return await super().update(obj_id=user.id, obj_in=user_in)

    async def issue_refresh(self, user: User) -> str:
        """
        Выпуск нового refresh токена и добавление его в redis по ключу user.id

        Args:
            user (User): Пользователь, которому нужно выдать refresh токен

        Returns:
            str: Новый refresh токен
        """
        refresh_token = self.token_service.create_refresh_token(user)
        await self.token_repository.add_token(
            token=refresh_token, user_id=user.id, expire_delta=settings.auth_jwt.refresh_token_expire_seconds
        )

        return refresh_token

    def issue_access(self, user: User) -> str:
        """
        Выпуск нового access токена

        Args:
            user (User): Пользователь, которому нужно выдать access токен
        """
        return self.token_service.create_access_token(user)

    async def issue_tokens(self, user: User) -> dict:
        """
        Выпуск новых refresh и access токенов

        Args:
            user (User): Пользователь, которому нужно выдать refresh и access токены

        Returns:
            dict: Словарь с refresh и access токенами
        """
        refresh_token = await self.issue_refresh(user=user)
        access_token = self.issue_access(user=user)

        return {"refresh_token": refresh_token, "access_token": access_token}

    async def issue_tokens_by_password(self, form_data: UserRegister) -> dict:
        """
        Выдача access и refresh токенов по логину и паролю

        Args:
            form_data (UserRegister): Данные о пользователе

        Returns:
            dict: Словарь с refresh и access токенами

        Raises:
            401 (unauthorized): Если логин или пароль неверные
        """
        user = await self.repository.get_one_by_field(value=form_data.username, field="username")
        if user:
            if self.passwords_manager.validate_password(
                password=form_data.password, hashed_password=user.hashed_password
            ):
                return await self.issue_tokens(user=user)

        raise INVALID_AUTHENTICATION_CREDENTIALS

    async def get_user_by_token(self, token: str) -> User:
        """
        Получение пользователя по токену

        Args:
            token (str): Токен

        Returns:
            User: Пользователь

        Raises:
            401 (unauthorized): Если токен неверный
        """
        pyload = self.token_service.decode_jwt(token=token)
        if pyload:
            user = await self.repository.get_obj_by_id(obj_id=int(pyload["sub"]))

            return user

    async def reissue_tokens_by_refresh(self, refresh_token: str) -> dict:
        """
        Перевыпуск токенов по предоставленному refresh

        Args:
            refresh_token (str): Refresh токен

        Returns:
            dict: Словарь с refresh и access токенами

        Raises:
            401 (unauthorized): Если refresh токен неверный или отсутствует.
        """
        if refresh_token:
            user = await self.get_user_by_token(token=refresh_token)
            if user:
                saved_token = await self.token_repository.get_token(user.id)
                if saved_token == refresh_token:
                    return await self.issue_tokens(user=user)

        raise INVALID_REFRESH_TOKEN

    async def has_permissions(self, access_token: str, permissions: list[str]) -> User:
        """
        Проверка действительности access токена и ограничение доступа к ресурсам по роли

        Args:
            access_token (str): Access токен

        Returns:
            User: Пользователь

        Raises:
            401 (unauthorized): Если access токен неверный
            403 (forbidden): Если у пользователя недостаточно прав
        """
        if access_token:
            user = await self.get_user_by_token(access_token)
            if user:
                if user.role in permissions:
                    return user

                raise FORBIDDEN

        raise INVALID_ACCESS_TOKEN

    async def update_password(self, user: User, credentials: UserChangePassword) -> User:
        """
        Обновление пароля

        Args:
            user (User): Пользователь
            credentials (UserChangePassword): Старый, новый и подтверждающий пароль

        Returns:
            User: Обновленный пользователь

        Raises:
            400 (bad request): Если новый и подтверждающий пароли не совпадают
            401 (unauthorized): Если старый пароль неверный
        """
        if credentials.new_password != credentials.confirm_password:
            raise PASSWORDS_MISMATCH

        if user.hashed_password != self.passwords_manager.hash_password(credentials.old_password):
            raise INVALID_AUTHENTICATION_CREDENTIALS

        password_schema = PasswordSchema(
            hashed_password=self.passwords_manager.hash_password(credentials.new_password),
        )
        return await super().update(obj_id=user.id, obj_in=password_schema)
