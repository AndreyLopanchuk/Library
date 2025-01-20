from redis import Redis

from src.core.database.redis import redis_client


class TokenRepository:
    """
    Репозиторий для работы с токенами

    Args:
        redis_client (Redis): Клиент Redis
    """

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def add_token(self, token: str, user_id: int, expire_delta: int) -> None:
        """
        Добавление токена в redis

        Args:
            token (str): Токен
            user_id (int): Идентификатор пользователя
            expire_delta (int): Время жизни токена
        """
        await self.redis_client.set(str(user_id), token, ex=expire_delta)

    async def delete_token(self, user_id: int) -> None:
        """
        Удаление токена из redis

        Args:
            user_id (int): Идентификатор пользователя
        """
        await self.redis_client.delete(user_id)

    async def get_token(self, user_id: int) -> str | None:
        """
        Получение токена из redis

        Args:
            user_id (int): Идентификатор пользователя

        Returns:
            str: Токен
            None: Если токен не был найден
        """
        token = await self.redis_client.get(user_id)
        if token:
            return token.decode("utf-8")


token_repository = TokenRepository(redis_client=redis_client)


def get_token_repository() -> TokenRepository:
    return token_repository
