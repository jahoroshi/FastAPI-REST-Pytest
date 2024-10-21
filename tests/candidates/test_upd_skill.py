import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_update_candidate_skill_success(async_client: AsyncClient, access_token, create_candidate_skill):
    headers = {"Authorization": f"Bearer {access_token}"}
    skill_id = create_candidate_skill["id"]
    payload = {
        "skill_name": "Python",
        "level": "advanced",
        "years_of_experience": 3,
        "last_used_year": 2023
    }

    response = await async_client.patch(f'/api/v1/candidates/skills/{skill_id}', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == skill_id
    assert response_data["skill"]["name"] == "Python"
    assert response_data["level"] == "advanced"
    assert response_data["years_of_experience"] == 3
    assert response_data["last_used_year"] == 2023


@pytest.mark.asyncio
async def test_update_candidate_skill_unauthorized(async_client: AsyncClient, create_candidate_skill):
    skill_id = create_candidate_skill["id"]
    payload = {
        "skill_name": "Python",
        "level": "advanced",
        "years_of_experience": 3,
        "last_used_year": 2023
    }

    response = await async_client.patch(f'/api/v1/candidates/skills/{skill_id}', json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_update_candidate_skill_not_found(async_client: AsyncClient, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    non_existent_skill_id = 9999
    payload = {
        "skill_name": "Python",
        "level": "advanced",
        "years_of_experience": 3,
        "last_used_year": 2023
    }

    response = await async_client.patch(f'/api/v1/candidates/skills/{non_existent_skill_id}', json=payload, headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Skill not found"}



@pytest.mark.asyncio
async def test_update_candidate_skill_invalid_level(async_client: AsyncClient, access_token, create_candidate_skill):
    headers = {"Authorization": f"Bearer {access_token}"}
    skill_id = create_candidate_skill["id"]
    payload = {
        "skill_name": "Python",
        "level": "invalid_level",
        "years_of_experience": 3,
        "last_used_year": 2023
    }

    response = await async_client.patch(f'/api/v1/candidates/skills/{skill_id}', json=payload, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_candidate_skill_invalid_years_of_experience(async_client: AsyncClient, access_token, create_candidate_skill):
    headers = {"Authorization": f"Bearer {access_token}"}
    skill_id = create_candidate_skill["id"]
    payload = {
        "skill_name": "Python",
        "level": "beginner",
        "years_of_experience": -1,
        "last_used_year": 2023
    }

    response = await async_client.patch(f'/api/v1/candidates/skills/{skill_id}', json=payload, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_candidate_skill_future_last_used_year(async_client: AsyncClient, access_token, create_candidate_skill):
    headers = {"Authorization": f"Bearer {access_token}"}
    skill_id = create_candidate_skill["id"]
    payload = {
        "skill_name": "Python",
        "level": "intermediate",
        "years_of_experience": 2,
        "last_used_year": 2050
    }

    response = await async_client.patch(f'/api/v1/candidates/skills/{skill_id}', json=payload, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_candidate_skill_partial_update(async_client: AsyncClient, access_token, create_candidate_skill):
    headers = {"Authorization": f"Bearer {access_token}"}
    skill_id = create_candidate_skill["id"]
    payload = {
        "skill_name": "Updated Skill Name"
    }

    response = await async_client.patch(f'/api/v1/candidates/skills/{skill_id}', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["skill"]["name"] == "Updated Skill Name"
