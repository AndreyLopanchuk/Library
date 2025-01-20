from typing import Type, Callable, Any
from unittest.mock import AsyncMock

import pytest

from src.core.schemas.user_schema import UserDB
from tests.unit_tests.mock_services import BaseMokService

test_data_full = UserDB(id=1, username="Иван", role="admin", hashed_password=b"123")


@pytest.fixture
async def mock_dependency():
    return AsyncMock()


@pytest.fixture(scope="function")
async def override_services_dependencies(mock_dependency, test_app, request):
    """
    Фикстура для зависимостей в тестах

    Args:
        mock_dependency (AsyncMock): экземпляр AsyncMock, который будет использоваться для мокирования зависимостей
        test_app (FastAPI): экземпляр приложения, которое будет использоваться для тестов.
        request (pytest.FixtureRequest): Объект запроса pytest. предоставляет доступ к параметрам теста.

    Yields:
        BaseMokService: Экземпляр класса BaseMokService, который будет использоваться в тестах.
    """
    service_class: Type[BaseMokService] = request.param["service_class"]
    dependency_function: Callable[..., Any] = request.param["dependency_function"]
    test_method_name: str = request.param["test_method_name"]
    service_instance: BaseMokService = service_class(
        dependency=mock_dependency, test_method_name=test_method_name, fake_data=test_data_full
    )

    def override_dependency(q: str | None = None):
        """
        определяет функцию, которая будет использоваться для замены зависимостей.

        Args:
            q (str | None, optional): Параметр q. Defaults to None.

        Returns:
            Any: возвращает экземпляр класса service_class
        """
        return service_instance

    test_app.dependency_overrides[dependency_function] = override_dependency
    yield service_instance
