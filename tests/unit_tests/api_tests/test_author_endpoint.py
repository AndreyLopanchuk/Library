import pytest

from src.auth.api.auth_dependencies import get_auth_service
from tests.unit_tests.mock_services import AuthService


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "override_services_dependencies",
    [
        {"service_class": AuthService, "dependency_function": get_auth_service, "test_method_name": "create_user"},
    ],
    indirect=True,
)
async def test_get_authors_endpoint(override_services_dependencies, test_client):
    response = await test_client.post("/auth/register/", data={"username": "user", "password": "1231"})
    print(response.json())
    assert response.status_code == 201
    assert response.json() == {"message": "Registration is completed", "username": "Иван"}
