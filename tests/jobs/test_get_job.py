import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_job_success(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    job_id = create_job["id"]

    response = await async_client.get(f'/api/v1/jobs/{job_id}', headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == job_id
    assert response_data["title"] == "Software Engineer"
    assert response_data["description"] == "We are looking for a Software Engineer."
    assert len(response_data["requirements"]) == 1
    assert response_data["requirements"][0]["skill"]["name"] == "Python"
    assert response_data["requirements"][0]["minimal_level"] == "beginner"
    assert response_data["requirements"][0]["minimal_years_of_experience"] == 0


@pytest.mark.asyncio
async def test_get_job_unauthorized(async_client: AsyncClient, create_job):
    job_id = create_job["id"]

    response = await async_client.get(f'/api/v1/jobs/{job_id}')

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_get_job_not_found(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    non_existent_job_id = 9999

    response = await async_client.get(f'/api/v1/jobs/{non_existent_job_id}', headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}
