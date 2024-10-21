from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserUpdateSchema, UserViewSchema
from src.candidates.schemas import UserCandidateViewSchema, CandidateViewSchema, UserCandidateUpdateSchema, \
    CandidateProfileUpdateSchema
from src.tools.database import update_model_instance
from src.tools.profile import check_role


async def get_candidate_profile_service(current_user, session: AsyncSession):
    await check_role(current_user, 'candidate')
    user = current_user
    candidate_profile = user.candidate_profile

    return UserCandidateViewSchema(
        user=UserViewSchema.from_orm(user),
        candidate_profile=CandidateViewSchema.from_orm(candidate_profile)
    )


async def update_candidate_profile_service(profile_data, current_user, session: AsyncSession):
    await check_role(current_user, 'candidate')
    user = current_user
    candidate_profile = user.candidate_profile

    user_dict = profile_data.user.dict(exclude_unset=True, exclude_none=True)
    candidate_dict = profile_data.candidate_profile.dict(exclude_unset=True, exclude_none=True)

    for instance, data_dict in ((user, user_dict), (candidate_profile, candidate_dict)):
        update_model_instance(instance, data_dict)

    await session.commit()
    return UserCandidateUpdateSchema(
        user=UserUpdateSchema.from_orm(user),
        candidate_profile=CandidateProfileUpdateSchema.from_orm(candidate_profile)
    )


async def delete_candidate_profile_service(current_user, session: AsyncSession):
    await check_role(current_user, 'candidate')
    user = current_user

    await session.delete(user)
    await session.commit()

    return Response(status_code=204)
