import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_delete_candidate_skill_success(async_client: AsyncClient, access_token, create_candidate_skill):
    headers = {"Authorization": f"Bearer {access_token}"}
    skill_id = create_candidate_skill["id"]

    response = await async_client.delete(f'/api/v1/candidates/skills/{skill_id}', headers=headers)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_candidate_skill_unauthorized(async_client: AsyncClient, create_candidate_skill):
    skill_id = create_candidate_skill["id"]

    response = await async_client.delete(f'/api/v1/candidates/skills/{skill_id}')

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_delete_candidate_skill_not_found(async_client: AsyncClient, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    non_existent_skill_id = 9999

    response = await async_client.delete(f'/api/v1/candidates/skills/{non_existent_skill_id}', headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Skill not found"}
