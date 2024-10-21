import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_update_job_success(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    job_id = create_job["id"]
    payload = {
        "title": "Updated Job Title",
        "description": "Updated job description."
    }

    response = await async_client.patch(f'/api/v1/jobs/update/{job_id}', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == job_id
    assert response_data["title"] == "Updated Job Title"
    assert response_data["description"] == "Updated job description."


@pytest.mark.asyncio
async def test_update_job_unauthorized(async_client: AsyncClient, create_job):
    job_id = create_job["id"]
    payload = {
        "title": "Updated Job Title",
        "description": "Updated job description."
    }

    response = await async_client.patch(f'/api/v1/jobs/update/{job_id}', json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_update_job_not_found(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    non_existent_job_id = 9999
    payload = {
        "title": "Updated Job Title",
        "description": "Updated job description."
    }

    response = await async_client.patch(f'/api/v1/jobs/update/{non_existent_job_id}', json=payload, headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}


@pytest.mark.asyncio
async def test_update_job_partial_update(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    job_id = create_job["id"]
    payload = {
        "title": "Partially Updated Job Title"
    }

    response = await async_client.patch(f'/api/v1/jobs/update/{job_id}', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == job_id
    assert response_data["title"] == "Partially Updated Job Title"


@pytest.mark.asyncio
async def test_update_job_part_data(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    job_id = create_job["id"]
    payload = {
        "title": "",
        "description": "Updated job description."
    }

    response = await async_client.patch(f'/api/v1/jobs/update/{job_id}', json=payload, headers=headers)

    assert response.status_code == 200
