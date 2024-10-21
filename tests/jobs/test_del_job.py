import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_delete_job_success(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    job_id = create_job["id"]

    response = await async_client.delete(f'/api/v1/jobs/delete/{job_id}', headers=headers)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_job_unauthorized(async_client: AsyncClient, create_job):
    job_id = create_job["id"]

    response = await async_client.delete(f'/api/v1/jobs/delete/{job_id}')

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_delete_job_not_found(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    non_existent_job_id = 9999

    response = await async_client.delete(f'/api/v1/jobs/delete/{non_existent_job_id}', headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}
