import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_add_candidate_skill_success(async_client: AsyncClient, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "skill_name": "Python",
        "level": "beginner",
        "years_of_experience": 0,
        "last_used_year": 2023
    }

    response = await async_client.post('/api/v1/candidates/skills/add_skill', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert "skill" in response_data
    assert response_data["skill"]["name"] == "Python"
    assert response_data["level"] == "beginner"
    assert response_data["years_of_experience"] == 0
    assert response_data["last_used_year"] == 2023


@pytest.mark.asyncio
async def test_add_candidate_skill_unauthorized(async_client: AsyncClient):
    payload = {
        "skill_name": "Python",
        "level": "beginner",
        "years_of_experience": 0,
        "last_used_year": 2023
    }

    response = await async_client.post('/api/v1/candidates/skills/add_skill', json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_add_candidate_skill_invalid_data(async_client: AsyncClient, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "skill_name": "",
        "level": "advanced",
        "years_of_experience": -1,
        "last_used_year": 2025
    }

    response = await async_client.post('/api/v1/candidates/skills/add_skill', json=payload, headers=headers)

    assert response.status_code == 422
