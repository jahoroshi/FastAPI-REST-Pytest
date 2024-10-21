import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database import Base
from database import get_session
from main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client():
    engine = create_async_engine(DATABASE_URL)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testemail@mail.com',
        'role': 'candidate'
    }


@pytest.fixture
def recruiter_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testemail@mail.com',
        'role': 'recruiter'
    }


@pytest_asyncio.fixture
async def access_token(async_client, user_data):
    reg_response = await async_client.post('/api/v1/auth/registration', json=user_data)

    response = await async_client.post('/api/v1/auth/token', json=user_data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    token_data = response.json()
    assert 'access_token' in token_data, f"Response does not contain 'access_token'. Response: {response.json()}"
    access_token = token_data['access_token']
    return access_token


@pytest_asyncio.fixture
async def access_token_recruiter(async_client, recruiter_data):
    await async_client.post('/api/v1/auth/registration', json=recruiter_data)

    response = await async_client.post('/api/v1/auth/token', json=recruiter_data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    token_data = response.json()
    assert 'access_token' in token_data, f"Response does not contain 'access_token'. Response: {response.json()}"
    access_token = token_data['access_token']
    return access_token


@pytest.mark.asyncio
@pytest_asyncio.fixture
async def create_candidate_skill(async_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "skill_name": "Python",
        "level": "beginner",
        "years_of_experience": 1,
        "last_used_year": 2023
    }

    response = await async_client.post('/api/v1/candidates/skills/add_skill', json=payload, headers=headers)

    assert response.status_code == 200, f"Skill creation failed: {response.json()}"
    return response.json()


@pytest_asyncio.fixture
async def create_job(async_client, access_token_recruiter):
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
    assert response.status_code == 200, f"Failed to create job: {response.json()}"
    return response.json()


@pytest_asyncio.fixture
async def create_jobs(async_client, access_token_recruiter):
    headers = {"Authorization": f"Bearer {access_token_recruiter}"}
    jobs_data = [
        {
            "title": "Software Engineer",
            "description": "We are looking for a Software Engineer.",
            "requirements": [
                {
                    "skill_name": "Python",
                    "minimal_level": "beginner",
                    "minimal_years_of_experience": 0
                }
            ]
        },
        {
            "title": "Data Scientist",
            "description": "We are looking for a Data Scientist.",
            "requirements": [
                {
                    "skill_name": "Data Analysis",
                    "minimal_level": "intermediate",
                    "minimal_years_of_experience": 1
                }
            ]
        }
    ]

    created_jobs = []
    for job_data in jobs_data:
        response = await async_client.post('/api/v1/jobs/add_job', json=job_data, headers=headers)
        assert response.status_code == 200, f"Failed to create job: {response.json()}"
        created_jobs.append(response.json())

    return created_jobs


@pytest_asyncio.fixture
async def create_candidate(async_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    candidate_data = [
        {"skill_name": "Python", "level": "beginner", "years_of_experience": 1, "last_used_year": 2023},
        {"skill_name": "JavaScript", "level": "intermediate", "years_of_experience": 2, "last_used_year": 2022},
        {"skill_name": "Django", "level": "advanced", "years_of_experience": 3, "last_used_year": 2021}
    ]
    created_candidates = []

    for data in candidate_data:
        response = await async_client.post('/api/v1/candidates/skills/add_skill', json=data, headers=headers)
        assert response.status_code == 200, f"Failed to create candidate skill: {response.json()}"
        created_candidates.append(response.json())

    return created_candidates


@pytest_asyncio.fixture
async def create_job_match(async_client, access_token_recruiter):
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
    return response.json()
