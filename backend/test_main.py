import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from main import app
from database import get_db


from unittest.mock import MagicMock, AsyncMock

async def override_get_db():
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result
    yield mock_session


app.dependency_overrides[get_db] = override_get_db


@pytest.mark.asyncio
async def test_login_wrong_password():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/login", json={
            "email": "test@test.com",
            "password": "wrongpassword"
        })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_tasks_without_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tasks")
    assert response.status_code == 401