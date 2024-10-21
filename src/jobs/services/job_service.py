from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Job, Skill, JobRequirement
from src.jobs.schemas import JobCreateSchema, JobUpdateSchema
from src.tools.database import get_object, update_model_instance
from src.tools.profile import check_role


async def create_job_service(job_data: JobCreateSchema, current_user, session: AsyncSession):
    await check_role(current_user, 'recruiter')
    recruiter_profile = current_user.recruiter_profile

    job = Job(
        title=job_data.title,
        description=job_data.description,
        recruiter_id=recruiter_profile.id,
    )

    session.add(job)
    await session.flush()

    for req in job_data.requirements:
        skill = await get_object(Skill, Skill.name == req.skill_name, session)

        if skill is None:
            skill = Skill(name=req.skill_name)
            session.add(skill)
            await session.commit()
            await session.refresh(skill)

        job_requirement = JobRequirement(
            job_id=job.id,
            skill_id=skill.id,
            minimal_level=req.minimal_level,
            minimal_years_of_experience=req.minimal_years_of_experience,
        )

        session.add(job_requirement)

    await session.commit()

    stmt = select(Job).options(selectinload(Job.requirements).selectinload(JobRequirement.skill)).where(Job.id == job.id)
    result = await session.execute(stmt)
    job = result.scalars().first()

    return job


async def get_job_service(job_id: int, current_user, session: AsyncSession):
    recruiter_profile = current_user.recruiter_profile
    job = await get_object(Job, Job.id == job_id, session)
    if job is None or job.recruiter_id != recruiter_profile.id:
        raise HTTPException(status_code=404, detail='Job not found')
    return job


async def get_job_list_service(current_user, session: AsyncSession):
    recruiter_profile = current_user.recruiter_profile

    query = select(Job).where(Job.recruiter_id == recruiter_profile.id)
    results = await session.execute(query)
    job_list = results.scalars().all()

    return job_list


async def delete_job_service(job_id: int, current_user, session: AsyncSession):
    recruiter_profile = current_user.recruiter_profile
    job = await get_object(Job, Job.id == job_id, session)

    if job is None or job.recruiter_id != recruiter_profile.id:
        raise HTTPException(status_code=404, detail='Job not found')

    await session.delete(job)
    await session.commit()
    return Response(status_code=204)


async def update_job_service(job_id: int, job_data: JobUpdateSchema, current_user, session: AsyncSession):
    recruiter_profile = current_user.recruiter_profile
    job = await get_object(Job, Job.id == job_id, session)

    if job is None or job.recruiter_id != recruiter_profile.id:
        raise HTTPException(status_code=404, detail='Job not found')

    job_data_dict = job_data.dict(exclude_unset=True, exclude_none=True)

    update_model_instance(job, job_data_dict)

    await session.commit()
    await session.refresh(job)
    return job
