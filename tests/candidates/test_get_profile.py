import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_candidate_profile_success(async_client: AsyncClient, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await async_client.get('/api/v1/candidates/profile', headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert "user" in response_data
    assert "username" in response_data["user"]
    assert "email" in response_data["user"]
    assert "id" in response_data["user"]
    assert "candidate_profile" in response_data
    assert "skills" in response_data["candidate_profile"]


@pytest.mark.asyncio
async def test_get_candidate_profile_unauthorized(async_client: AsyncClient):
    response = await async_client.get('/api/v1/candidates/profile')

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
