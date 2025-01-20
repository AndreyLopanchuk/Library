import datetime

import jwt
from jwt import InvalidTokenError

from src.core.models.user_model import User
from src.core.config import settings


class JWTokenManager:
    """
    Сервисный класс для работы с токенами.
    """

    def encode_jwt(
        self,
        payload: dict,
        expire_seconds: int,
        private_key=settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    ) -> str:
        """
        Кодирует токен приватным ключом.

        Args:
            payload (dict): Тело токена.
            expire_seconds (int): Срок действия токена.
            private_key (str): Приватный ключ.
            algorithm (str): Алгоритм кодирования.

        Returns:
            str: Строка с закодированным токеном.
        """
        to_encode = payload.copy()
        now = datetime.datetime.now(datetime.UTC)
        expire = now + datetime.timedelta(seconds=expire_seconds)
        to_encode.update({"exp": expire, "iat": now})

        return jwt.encode(to_encode, private_key, algorithm=algorithm)

    def decode_jwt(
        self,
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    ) -> dict | None:
        """
        Декодирует токен публичным ключом.

        Args:
            token (str): Закодированный токен.
            public_key (str): Публичный ключ.
            algorithm (str): Алгоритм декодирования.

        Returns:
            dict: Словарь с данными токена.
            None: Если токен неверный.
        """
        try:
            decoded = jwt.decode(token, public_key, algorithms=[algorithm])
            return decoded

        except InvalidTokenError:
            return None

    def create_token(self, token_type: str, token_data: dict, expire_seconds: int) -> str:
        """
        Cоздает токен.

        Args:
            token_type (str): Тип токена.
            token_data (dict): Данные токена.
            expire_seconds (int): Срок действия токена.

        Returns:
            str: Строка с закодированным токеном.
        """
        jwt_payload = {"type": token_type}
        jwt_payload.update(token_data)

        return self.encode_jwt(
            payload=jwt_payload,
            expire_seconds=expire_seconds,
        )

    def create_access_token(self, user: User) -> str:
        """
        Создает access токен.

        Args:
            user (User): Пользователь которому нужно выдать access токен.

        Returns:
            str: Строка с закодированным access токеном.
        """
        jwt_payload = {"sub": str(user.id), "username": user.username}
        return self.create_token(
            token_type="access",
            token_data=jwt_payload,
            expire_seconds=settings.auth_jwt.access_token_expire_seconds,
        )

    def create_refresh_token(self, user: User) -> str:
        """
        Создает refresh токен.

        Args:
            user (User): Пользователь которому нужно выдать refresh токен.

        Returns:
            str: Строка с закодированным refresh токеном.
        """
        jwt_payload = {"sub": str(user.id), "username": user.username}
        return self.create_token(
            token_type="refresh",
            token_data=jwt_payload,
            expire_seconds=settings.auth_jwt.refresh_token_expire_seconds,
        )


token_service = JWTokenManager()


def get_token_service() -> JWTokenManager:
    return token_service
