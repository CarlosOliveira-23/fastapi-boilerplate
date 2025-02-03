import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_start_task(client: AsyncClient):
    """Testa se uma tarefa assíncrona é iniciada corretamente."""
    response = await client.post("/tasks/start-task/test-task")
    assert response.status_code == 200
    assert "task_id" in response.json()
