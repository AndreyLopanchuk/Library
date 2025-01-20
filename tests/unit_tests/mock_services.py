from typing import Any
from unittest.mock import AsyncMock


class BaseMokService:
    """
    Базовый класс для мокирования.

    Args:
        dependency (AsyncMock): Мок зависимости (экземпляр AsyncMock, который представляет собой мокированный объект,
            который будет использоваться вместо реального сервиса.).
        test_method_name (str): Название тестового метода, который будет создан в классе для мокирования.
        fake_data (Any, optional): данные, которые будут возвращены мокированным методом.

    Attributes:
        _dependency (AsyncMock): Мок зависимости.
        _dependency.some_method.return_value (Any): Фейковые данные.
    """

    def __init__(self, dependency: AsyncMock, test_method_name: str, fake_data: Any = None):
        self._dependency = dependency
        self._dependency.some_method.return_value = fake_data

        async def method(*args, **kwargs):
            """
            определяет новый асинхронный метод, который будет создан в классе.
            метод принимает любые аргументы (*args и **kwargs) и игнорирует их.
            """
            return await self._dependency.some_method()

        setattr(self, test_method_name, method)


class AuthService(BaseMokService):
    """Мок класса сервиса авторизации"""

    pass
