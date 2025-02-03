import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    """Testa login e geração de token JWT."""
    response = await client.post("/auth/login", json={
        "username": "testuser",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
