from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from src.auth.schemas import UserUpdateSchema, UserViewSchema
from src.recruiters.schemas import UserRecruiterViewSchema, RecruiterViewSchema, UserRecruiterUpdateSchema, RecruiterUpdateSchema
from src.tools.profile import check_role


async def get_object(model, filter_by, session):
    query = select(model).where(filter_by)
    result = await session.execute(query)
    obj = result.scalar_one_or_none()
    return obj


def update_model_instance(instance, data):
    for key, value in data.items():
        setattr(instance, key, value)


async def get_recruiter_profile_service(current_user, session: AsyncSession):
    await check_role(current_user, 'recruiter')
    user = await get_object(User, User.id == current_user.id, session)
    recruiter_profile = user.recruiter_profile

    return UserRecruiterViewSchema(
        user=UserViewSchema.from_orm(user),
        recruiter_profile=RecruiterViewSchema.from_orm(recruiter_profile)
    )


async def update_recruiter_profile_service(profile_data, current_user, session: AsyncSession):
    await check_role(current_user, 'recruiter')
    user = await get_object(User, User.id == current_user.id, session)
    recruiter_profile = user.recruiter_profile

    user_dict = profile_data.user.dict(exclude_unset=True, exclude_none=True)
    recruiter_dict = profile_data.recruiter_profile.dict(exclude_unset=True, exclude_none=True)

    for instance, data_dict in ((user, user_dict), (recruiter_profile, recruiter_dict)):
        update_model_instance(instance, data_dict)

    await session.commit()
    return UserRecruiterUpdateSchema(
        user=UserUpdateSchema.from_orm(user),
        recruiter_profile=RecruiterUpdateSchema.from_orm(recruiter_profile)
    )


async def delete_recruiter_profile_service(current_user, session: AsyncSession):
    await check_role(current_user, 'recruiter')
    user = await get_object(User, User.id == current_user.id, session)

    await session.delete(user)
    await session.commit()

    return Response(status_code=204)
