import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Testa o cadastro de um usuário."""
    response = await client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
        "role": "user"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    """Testa a busca de um usuário cadastrado."""
    response = await client.get("/users/testuser")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


@pytest.mark.asyncio
async def test_admin_only_route(client: AsyncClient):
    """Testa se um usuário comum é bloqueado na rota de admin."""
    response = await client.get("/users/admin-only")
    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission"
