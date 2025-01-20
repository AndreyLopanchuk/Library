import pytest


@pytest.mark.asyncio
async def test_create_author_endpoint(test_client) -> None:
    response = await test_client.post("/authors/")
    assert response.status_code == 401
