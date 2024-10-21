from fastapi import APIRouter, Depends

from database import get_session
from src.auth.services import token_service
from src.candidates.schemas import CandidateSkillCreateSchema, CandidateSkillViewSchema, \
    CandidateSkillUpdateSchema, UserCandidateViewSchema, UserCandidateUpdateSchema
from src.candidates.services.profile_service import (
    get_candidate_profile_service,
    update_candidate_profile_service,
    delete_candidate_profile_service
)
from src.candidates.services.skill_service import (
    add_candidate_skill_service,
    update_candidate_skill_service,
    delete_candidate_skill_service
)

router_profile = APIRouter(
    prefix="/candidates",
    tags=["Candidate Profile"],
)

router_skill = APIRouter(
    prefix="/candidates/skills",
    tags=["Candidate Skills"],
)

@router_profile.get("/profile", response_model=UserCandidateViewSchema, responses={
    200: {"description": "Profile retrieved successfully."},
    401: {"description": "User not authenticated."},
    404: {"description": "Profile not found."},
})
async def get_candidate_profile(current_user=Depends(token_service.get_current_user), session=Depends(get_session)):
    """
    Retrieve related Candidate Profile and User models.
    Candidate profile extends User.
    """
    return await get_candidate_profile_service(current_user, session)


@router_profile.patch('/update', response_model=UserCandidateUpdateSchema, responses={
    200: {"description": "Profile updated successfully."},
    400: {"description": "Invalid data."},
    401: {"description": "User not authenticated."},
})
async def update_candidate_profile(
        profile_data: UserCandidateUpdateSchema,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Update two related models: Candidate Profile and User.
    """
    return await update_candidate_profile_service(profile_data, current_user, session)


@router_profile.delete('/delete', responses={
    204: {"description": "Profile deleted successfully."},
    401: {"description": "User not authenticated."},
    404: {"description": "Profile not found."},
})
async def delete_candidate_profile(
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Deletes the User model, cascade.
    """
    return await delete_candidate_profile_service(current_user, session)


@router_skill.post('/add_skill', response_model=CandidateSkillViewSchema, responses={
    201: {"description": "Skill added successfully."},
    400: {"description": "Invalid data."},
    401: {"description": "User not authenticated."},
})
async def add_candidate_skill(
        skill_data: CandidateSkillCreateSchema,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    return await add_candidate_skill_service(skill_data, current_user, session)


@router_skill.patch('/{skill_id}', response_model=CandidateSkillViewSchema, responses={
    200: {"description": "Skill updated successfully."},
    400: {"description": "User already has a skill with this name."},
    401: {"description": "User not authenticated."},
    404: {"description": "Skill not found."},
})
async def update_candidate_skill(
        skill_data: CandidateSkillUpdateSchema,
        skill_id: int,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Retrieve skill information by ID.
    """
    return await update_candidate_skill_service(skill_data, skill_id, current_user, session)


@router_skill.delete('/{skill_id}', responses={
    204: {"description": "Skill deleted successfully."},
    401: {"description": "User not authenticated."},
    404: {"description": "Skill not found."},
})
async def delete_candidate_skill(
        skill_id: int,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    return await delete_candidate_skill_service(skill_id, current_user, session)
