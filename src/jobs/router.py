from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from database import get_session
from src.auth.services import token_service
from src.jobs.schemas import JobCreateSchema, JobViewSchema, JobUpdateSchema, JobRequirementSchema, \
    JobRequirementViewSchema, JobRequirementUpdateSchema
from src.jobs.services.job_service import (
    create_job_service,
    get_job_service,
    get_job_list_service,
    delete_job_service,
    update_job_service,
)
from src.jobs.services.requirement_service import (
    add_requirement_service,
    delete_requirement_service,
    update_requirement_service,
)

router_job = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

router_req = APIRouter(
    prefix="/job/requirements",
    tags=["Job Requirements"],
)

@router_job.post('/add_job', response_model=JobViewSchema, responses={
    201: {"description": "Job created successfully."},
    400: {"description": "Invalid data."},
    401: {"description": "User not authenticated."},
})
async def create_job(
        job_data: JobCreateSchema,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Create a new job. Multiple "requirements" can be specified or left empty.

    "skill_name": "string",
    "minimal_level": "beginner/intermediate/advanced",
    "minimal_years_of_experience": Integer (Years)
    """
    return await create_job_service(job_data, current_user, session)


@router_job.get('/{job_id}', response_model=JobViewSchema, responses={
    200: {"description": "Job retrieved successfully."},
    401: {"description": "User not authenticated."},
    404: {"description": "Job not found."},
})
async def get_job(
        job_id: int,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Retrieve job information by ID.
    """
    return await get_job_service(job_id, current_user, session)


@router_job.get('/get_jobs/', response_model=List[JobViewSchema], responses={
    200: {"description": "List of jobs retrieved successfully."},
    401: {"description": "User not authenticated."},
})
async def get_job_list(
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    return await get_job_list_service(current_user, session)


@router_job.delete('/delete/{job_id}', responses={
    204: {"description": "Job deleted successfully."},
    401: {"description": "User not authenticated."},
    404: {"description": "Job not found."},
})
async def delete_job(
        job_id: int,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    return await delete_job_service(job_id, current_user, session)


@router_job.patch('/update/{job_id}', response_model=JobViewSchema, responses={
    200: {"description": "Job updated successfully."},
    400: {"description": "Invalid data."},
    401: {"description": "User not authenticated."},
    404: {"description": "Job not found."},
})
async def update_job(
        job_id: int,
        job_data: JobUpdateSchema,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Only job parameters can be changed; requirements are added, edited, or deleted separately.
    """
    return await update_job_service(job_id, job_data, current_user, session)


@router_req.post('/add/{job_id}', response_model=JobViewSchema, responses={
    201: {"description": "Requirement added successfully."},
    400: {"description": "Invalid data."},
    401: {"description": "User not authenticated."},
    404: {"description": "Job not found."},
})
async def add_requirement(
        job_id: int,
        req_data: JobRequirementSchema,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    return await add_requirement_service(job_id, req_data, current_user, session)


@router_req.patch('/update/{req_id}', response_model=JobRequirementViewSchema, responses={
    200: {"description": "Requirement updated successfully."},
    400: {"description": "Invalid data."},
    401: {"description": "User not authenticated."},
    404: {"description": "Requirement not found."},
})
async def update_requirement(
        req_id: int,
        req_data: JobRequirementUpdateSchema,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    return await update_requirement_service(req_id, req_data, current_user, session)


@router_req.delete('/delete/{req_id}', responses={
    204: {"description": "Requirement deleted successfully."},
    401: {"description": "User not authenticated."},
    404: {"description": "Requirement not found."},
})
async def delete_requirement(
        req_id: int,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    return await delete_requirement_service(req_id, current_user, session)
