import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_job_list_success(async_client: AsyncClient, access_token_recruiter, create_jobs):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}

    response = await async_client.get('/api/v1/jobs/get_jobs/', headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) >= 2
    job_titles = [job["title"] for job in response_data]
    assert "Software Engineer" in job_titles
    assert "Data Scientist" in job_titles


@pytest.mark.asyncio
async def test_get_job_list_unauthorized(async_client: AsyncClient):
    response = await async_client.get('/api/v1/jobs/get_jobs/')

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
