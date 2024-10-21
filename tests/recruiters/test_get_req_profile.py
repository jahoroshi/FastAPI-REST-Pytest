import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_recruiter_profile_success(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}

    response = await async_client.get('/api/v1/recruiters/profile', headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert "user" in response_data
    assert "username" in response_data["user"]
    assert "email" in response_data["user"]
    assert "id" in response_data["user"]
    assert "recruiter_profile" in response_data
    assert "company_name" in response_data["recruiter_profile"]


@pytest.mark.asyncio
async def test_get_recruiter_profile_unauthorized(async_client: AsyncClient):
    response = await async_client.get('/api/v1/recruiters/profile')

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_get_recruiter_profile_not_found(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}

    await async_client.delete('/api/v1/recruiters/delete', headers=headers)

    response = await async_client.get('/api/v1/recruiters/profile', headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}
