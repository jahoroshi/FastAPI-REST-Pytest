from fastapi import APIRouter, Depends

from database import get_session
from src.auth.services import token_service
from src.recruiters.schemas import UserRecruiterViewSchema, UserRecruiterUpdateSchema
from src.recruiters.services.profile_service import (
    get_recruiter_profile_service,
    update_recruiter_profile_service,
    delete_recruiter_profile_service
)

router_profile = APIRouter(
    prefix="/recruiters",
    tags=["Recruiter Profile"],
)

@router_profile.get("/profile", response_model=UserRecruiterViewSchema, responses={
    200: {"description": "Recruiter profile retrieved successfully."},
    401: {"description": "User not authenticated."},
    404: {"description": "Recruiter profile not found."},
})
async def get_recruiter_profile(
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Retrieve related Recruiter Profile and User models.
    Recruiter profile extends User.
    """
    return await get_recruiter_profile_service(current_user, session)


@router_profile.patch('/update', response_model=UserRecruiterUpdateSchema, responses={
    200: {"description": "Recruiter profile updated successfully."},
    400: {"description": "Invalid data."},
    401: {"description": "User not authenticated."},
})
async def update_recruiter_profile(
        profile_data: UserRecruiterUpdateSchema,
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Update two related models: Recruiter Profile and User.
    """
    return await update_recruiter_profile_service(profile_data, current_user, session)


@router_profile.delete('/delete', responses={
    204: {"description": "Recruiter profile deleted successfully."},
    401: {"description": "User not authenticated."},
    404: {"description": "Recruiter profile not found."},
})
async def delete_recruiter_profile(
        current_user=Depends(token_service.get_current_user),
        session=Depends(get_session)):
    """
    Deletes the User model, cascade.
    """
    return await delete_recruiter_profile_service(current_user, session)
