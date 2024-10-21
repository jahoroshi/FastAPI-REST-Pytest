import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_job_success(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    payload = {
        "title": "Software Engineer",
        "description": "We are looking for a Software Engineer.",
        "requirements": [
            {
                "skill_name": "Python",
                "minimal_level": "beginner",
                "minimal_years_of_experience": 0
            }
        ]
    }

    response = await async_client.post('/api/v1/jobs/add_job', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Software Engineer"
    assert response_data["description"] == "We are looking for a Software Engineer."
    assert len(response_data["requirements"]) == 1
    assert response_data["requirements"][0]["skill"]["name"] == "Python"
    assert response_data["requirements"][0]["minimal_level"] == "beginner"
    assert response_data["requirements"][0]["minimal_years_of_experience"] == 0


@pytest.mark.asyncio
async def test_create_job_unauthorized(async_client: AsyncClient):
    payload = {
        "title": "Software Engineer",
        "description": "We are looking for a Software Engineer.",
        "requirements": [
            {
                "skill_name": "Python",
                "minimal_level": "beginner",
                "minimal_years_of_experience": 0
            }
        ]
    }

    response = await async_client.post('/api/v1/jobs/add_job', json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_create_job_without_requirements(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    payload = {
        "title": "Software Engineer",
        "description": "We are looking for a Software Engineer.",
        "requirements": []
    }

    response = await async_client.post('/api/v1/jobs/add_job', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Software Engineer"
    assert response_data["description"] == "We are looking for a Software Engineer."
    assert response_data["requirements"] == []


@pytest.mark.asyncio
async def test_create_job_invalid_level(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    payload = {
        "title": "Software Engineer",
        "description": "We are looking for a Software Engineer.",
        "requirements": [
            {
                "skill_name": "Python",
                "minimal_level": "invalid_level",
                "minimal_years_of_experience": 0
            }
        ]
    }

    response = await async_client.post('/api/v1/jobs/add_job', json=payload, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_job_missing_fields(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    payload = {
        "title": "",
        "description": "We are looking for a Software Engineer."
    }

    response = await async_client.post('/api/v1/jobs/add_job', json=payload, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_job_partial_requirements(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    payload = {
        "title": "Software Engineer",
        "description": "We are looking for a Software Engineer.",
        "requirements": [
            {
                "skill_name": "Python",
                "minimal_level": "beginner"
            }
        ]
    }

    response = await async_client.post('/api/v1/jobs/add_job', json=payload, headers=headers)

    assert response.status_code == 422
