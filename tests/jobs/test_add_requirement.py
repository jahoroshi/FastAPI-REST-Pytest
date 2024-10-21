import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_requirement_success(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    job_id = create_job["id"]
    payload = {
        "skill_name": "Django",
        "minimal_level": "intermediate",
        "minimal_years_of_experience": 1
    }

    response = await async_client.post(f'/api/v1/job/requirements/add/{job_id}', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == job_id
    assert len(response_data["requirements"]) == 2
    assert response_data["requirements"][-1]["skill"]["name"] == "Django"
    assert response_data["requirements"][-1]["minimal_level"] == "intermediate"
    assert response_data["requirements"][-1]["minimal_years_of_experience"] == 1


@pytest.mark.asyncio
async def test_add_requirement_unauthorized(async_client: AsyncClient, create_job):
    job_id = create_job["id"]
    payload = {
        "skill_name": "Django",
        "minimal_level": "intermediate",
        "minimal_years_of_experience": 1
    }

    response = await async_client.post(f'/api/v1/job/requirements/add/{job_id}', json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_add_requirement_not_found(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    non_existent_job_id = 9765
    payload = {
        "skill_name": "Django",
        "minimal_level": "intermediate",
        "minimal_years_of_experience": 1
    }

    response = await async_client.post(f'/api/v1/job/requirements/add/{non_existent_job_id}', json=payload, headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}


@pytest.mark.asyncio
async def test_add_requirement_clone(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    job_id = create_job["id"]
    payload = {
        "skill_name": "FastAPI",
        "minimal_level": "advanced",
        "minimal_years_of_experience": 2
    }

    await async_client.post(f'/api/v1/job/requirements/add/{job_id}', json=payload, headers=headers)

    response = await async_client.post(f'/api/v1/job/requirements/add/{job_id}', json=payload, headers=headers)

    assert response.status_code == 409

@pytest.mark.asyncio
async def test_add_requirement_invalid_level(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    job_id = create_job["id"]
    payload = {
        "skill_name": "Django",
        "minimal_level": "invalid_level",
        "minimal_years_of_experience": 1
    }

    response = await async_client.post(f'/api/v1/job/requirements/add/{job_id}', json=payload, headers=headers)

    assert response.status_code == 422
    response_data = response.json()
    assert "minimal_level" in response_data["detail"][0]["loc"]
    assert response_data["detail"][0]["msg"] == "Input should be 'beginner', 'intermediate' or 'advanced'"





