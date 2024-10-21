from typing import List

from fastapi import APIRouter, Depends, HTTPException

from database import get_session
from src.auth.services import token_service
from src.candidates.schemas import UserCandidateViewSchema
from src.jobs.schemas import JobViewSchema
from src.matching.services.matching_service import (
    get_matching_candidates_service,
    get_matching_jobs_service
)

router = APIRouter(
    tags=["Matching"],
)
@router.get("/jobs/{job_id}/candidates", response_model=List[UserCandidateViewSchema], responses={
    200: {"description": "Matching candidates retrieved successfully."},
    401: {"description": "User not authenticated."},
    404: {"description": "Job not found."},
})
async def get_matching_candidates(
        job_id: int,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Returns candidates matching the job. Candidate skills are sorted by relevance to job requirements.
    """
    return await get_matching_candidates_service(job_id, current_user, session)


@router.get("/candidate/matching-jobs", response_model=List[JobViewSchema], responses={
    200: {"description": "Matching jobs retrieved successfully."},
    401: {"description": "User not authenticated."},
})
async def get_matching_jobs(
        session=Depends(get_session),
        current_user=Depends(token_service.get_current_user)):
    """
    Returns jobs matching the candidate's profile.
    """
    return await get_matching_jobs_service(current_user, session)
