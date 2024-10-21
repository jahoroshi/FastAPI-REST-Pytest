import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_delete_candidate_profile_success(async_client: AsyncClient, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await async_client.delete('/api/v1/candidates/delete', headers=headers)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_candidate_profile_unauthorized(async_client: AsyncClient):
    response = await async_client.delete('/api/v1/candidates/delete')

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_delete_candidate_profile_not_found(async_client: AsyncClient, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    await async_client.delete('/api/v1/candidates/delete', headers=headers)

    response = await async_client.delete('/api/v1/candidates/delete', headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found.'}
