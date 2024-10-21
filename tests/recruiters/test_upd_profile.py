import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_update_recruiter_profile_success(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    payload = {
        "user": {
            "username": "updated_recruiter",
            "email": "updated_recruiter@mail.com"
        },
        "recruiter_profile": {
            "company_name": "Updated Company Name"
        }
    }

    response = await async_client.patch('/api/v1/recruiters/update', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user"]["username"] == "updated_recruiter"
    assert response_data["user"]["email"] == "updated_recruiter@mail.com"
    assert response_data["recruiter_profile"]["company_name"] == "Updated Company Name"


@pytest.mark.asyncio
async def test_update_recruiter_profile_unauthorized(async_client: AsyncClient):
    payload = {
        "user": {
            "username": "updated_recruiter",
            "email": "updated_recruiter@mail.com"
        },
        "recruiter_profile": {
            "company_name": "Updated Company Name"
        }
    }

    response = await async_client.patch('/api/v1/recruiters/update', json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_update_recruiter_profile_invalid_email(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    payload = {
        "user": {
            "username": "updated_recruiter",
            "email": "invalid_email"
        },
        "recruiter_profile": {
            "company_name": "Updated Company Name"
        }
    }

    response = await async_client.patch('/api/v1/recruiters/update', json=payload, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_recruiter_profile_missing_fields(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    payload = {
        "user": {
            "username": ""
        }
    }

    response = await async_client.patch('/api/v1/recruiters/update', json=payload, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_recruiter_profile_partial_update(async_client: AsyncClient, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    payload = {
        "user": {},
        "recruiter_profile": {
            "company_name": "Partially Updated Company"
        }
    }

    response = await async_client.patch('/api/v1/recruiters/update', json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["recruiter_profile"]["company_name"] == "Partially Updated Company"
