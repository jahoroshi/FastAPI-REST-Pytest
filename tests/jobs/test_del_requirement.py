import pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_delete_requirement_success(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    requirement_id = create_job["requirements"][0]["id"]

    response = await async_client.delete(f'/api/v1/job/requirements/delete/{requirement_id}', headers=headers)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_requirement_unauthorized(async_client: AsyncClient, create_job):
    requirement_id = create_job["requirements"][0]["id"]

    response = await async_client.delete(f'/api/v1/job/requirements/delete/{requirement_id}')

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_delete_requirement_not_found(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    non_existent_requirement_id = 9999

    response = await async_client.delete(f'/api/v1/job/requirements/delete/{non_existent_requirement_id}', headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Requirement not found"}
