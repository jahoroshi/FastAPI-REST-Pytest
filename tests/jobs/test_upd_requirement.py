import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_update_requirement_success(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    requirement_id = create_job["requirements"][0]["id"]
    payload = {
        "skill_name": "Django",
        "minimal_level": "intermediate",
        "minimal_years_of_experience": 2
    }

    response = await async_client.patch(f'/api/v1/job/requirements/update/{requirement_id}', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == requirement_id
    assert response_data["skill"]["name"] == "Django"
    assert response_data["minimal_level"] == "intermediate"
    assert response_data["minimal_years_of_experience"] == 2


@pytest.mark.asyncio
async def test_update_requirement_unauthorized(async_client: AsyncClient, create_job):
    requirement_id = create_job["requirements"][0]["id"]
    payload = {
        "skill_name": "Django",
        "minimal_level": "intermediate",
        "minimal_years_of_experience": 2
    }

    response = await async_client.patch(f'/api/v1/job/requirements/update/{requirement_id}', json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_update_requirement_not_found(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    non_existent_requirement_id = 9999
    payload = {
        "skill_name": "Django",
        "minimal_level": "intermediate",
        "minimal_years_of_experience": 2
    }

    response = await async_client.patch(f'/api/v1/job/requirements/update/{non_existent_requirement_id}', json=payload, headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Requirement not found"}


@pytest.mark.asyncio
async def test_update_requirement_invalid_data(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    requirement_id = create_job["requirements"][0]["id"]
    payload = {
        "skill_name": "",
        "minimal_level": "advanced",
        "minimal_years_of_experience": -1
    }

    response = await async_client.patch(f'/api/v1/job/requirements/update/{requirement_id}', json=payload, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_requirement_invalid_level(async_client: AsyncClient, access_token_recruiter, create_job):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    requirement_id = create_job["requirements"][0]["id"]
    payload = {
        "skill_name": "Django",
        "minimal_level": "invalid_level",
        "minimal_years_of_experience": 2
    }

    response = await async_client.patch(f'/api/v1/job/requirements/update/{requirement_id}', json=payload, headers=headers)

    assert response.status_code == 422
    response_data = response.json()
    assert "minimal_level" in response_data["detail"][0]["loc"]
    assert response_data["detail"][0]["msg"] == "Input should be 'beginner', 'intermediate' or 'advanced'"
