import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_matching_candidates(async_client: AsyncClient, access_token, access_token_recruiter,
                                       create_candidate):
    recruiter_data = {
        "username": "recruiteruser",
        "password": "recruiterpassword",
        "email": "recruiteremail@mail.com",
        "role": "recruiter"
    }

    response = await async_client.post('/api/v1/auth/registration', json=recruiter_data)
    if response.status_code == 400:
        print(f"Registration error: {response.json()}")
    assert response.status_code == 200, f"Failed to register recruiter: {response.json()}"

    response = await async_client.post('/api/v1/auth/token', json={
        "username": recruiter_data["username"],
        "password": recruiter_data["password"]
    })
    assert response.status_code == 200, f"Failed to obtain recruiter token: {response.json()}"
    access_token_recruiter = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token_recruiter}"}

    payload = {
        "title": "Software Engineer",
        "description": "We are looking for a Software Engineer.",
        "requirements": [
            {"skill_name": "Python", "minimal_level": "beginner", "minimal_years_of_experience": 0},
            {"skill_name": "JavaScript", "minimal_level": "intermediate", "minimal_years_of_experience": 2},
            {"skill_name": "Django", "minimal_level": "advanced", "minimal_years_of_experience": 3}
        ]
    }

    response = await async_client.post('/api/v1/jobs/add_job', json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Failed to create job: {response.json()}")
    assert response.status_code == 200, f"Failed to create job: {response.json()}"
    created_job = response.json()

    job_id = created_job["id"]

    response = await async_client.get(f'/api/v1/jobs/{job_id}/candidates', headers=headers)

    assert response.status_code == 200
    response_data = response.json()

    assert len(response_data) >= 1
    candidate_usernames = [candidate["user"]["username"] for candidate in response_data]

    for candidate in response_data:
        assert "user" in candidate
        assert "candidate_profile" in candidate
        assert isinstance(candidate["candidate_profile"]["skills"], list)
