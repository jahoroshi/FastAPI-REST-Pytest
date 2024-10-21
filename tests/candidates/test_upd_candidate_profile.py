import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_update_candidate_profile_success(async_client: AsyncClient, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "user": {
            "username": "updateduser",
            "email": "updatedemail@mail.com"
        },
        "candidate_profile": {}
    }

    response = await async_client.patch('/api/v1/candidates/update', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user"]["username"] == "updateduser"
    assert response_data["user"]["email"] == "updatedemail@mail.com"


@pytest.mark.asyncio
async def test_update_candidate_profile_unauthorized(async_client: AsyncClient):
    payload = {
        "user": {
            "username": "unauthorizeduser",
            "email": "unauthorized@mail.com"
        },
        "candidate_profile": {}
    }

    response = await async_client.patch('/api/v1/candidates/update', json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_update_candidate_profile_invalid_data(async_client: AsyncClient, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "user": {
            "username": "",
            "email": "invalidemail"
        },
        "candidate_profile": {}
    }

    response = await async_client.patch('/api/v1/candidates/update', json=payload, headers=headers)

    assert response.status_code == 422


