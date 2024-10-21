from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models import Job, Skill, JobRequirement
from src.jobs.schemas import JobRequirementSchema, JobRequirementUpdateSchema
from src.tools.database import update_model_instance, get_object


async def add_requirement_service(job_id: int, req_data: JobRequirementSchema, current_user, session: AsyncSession):
    recruiter_profile = current_user.recruiter_profile
    job = await get_object(Job, Job.id == job_id, session)

    if job is None or job.recruiter_id != recruiter_profile.id:
        raise HTTPException(status_code=404, detail='Job not found')

    skill = await get_object(Skill, Skill.name == req_data.skill_name, session)

    try:
        if skill is None:
            skill = Skill(name=req_data.skill_name)
            session.add(skill)
            await session.commit()
            await session.refresh(skill)

        job_requirement = JobRequirement(
            job_id=job.id,
            skill_id=skill.id,
            minimal_level=req_data.minimal_level,
            minimal_years_of_experience=req_data.minimal_years_of_experience,
        )

        session.add(job_requirement)
        await session.commit()

    except IntegrityError:
        raise HTTPException(status_code=409, detail='Requirements with these parameters already exist.')

    await session.refresh(job_requirement)
    await session.refresh(job)
    return job


async def delete_requirement_service(req_id: int, current_user, session: AsyncSession):
    recruiter_profile = current_user.recruiter_profile
    job_requirement = await get_object(JobRequirement, JobRequirement.id == req_id, session)
    if job_requirement is None:
        raise HTTPException(status_code=404, detail='Requirement not found')
    job = job_requirement.job

    if job.recruiter_id != recruiter_profile.id:
        raise HTTPException(status_code=404, detail='Requirement not found')

    await session.delete(job_requirement)
    await session.commit()
    return Response(status_code=204)


async def update_requirement_service(req_id: int, req_data: JobRequirementUpdateSchema, current_user, session: AsyncSession):
    recruiter_profile = current_user.recruiter_profile
    job_requirement = await get_object(JobRequirement, JobRequirement.id == req_id, session)

    if job_requirement is None:
        raise HTTPException(status_code=404, detail='Requirement not found')

    job = job_requirement.job

    if job.recruiter_id != recruiter_profile.id:
        raise HTTPException(status_code=404, detail='Requirement not found')

    if job_requirement.skill.name != req_data.skill_name and req_data.skill_name is not None:
        skill = await get_object(Skill, Skill.name == req_data.skill_name, session)

        if skill is None:
            skill = Skill(name=req_data.skill_name)
            session.add(skill)
            await session.commit()
            await session.refresh(skill)

        job_requirement.skill_id = skill.id
        await session.flush()

    query = select(JobRequirement).where(JobRequirement.job_id == job.id)
    result = await session.execute(query)
    req_list = result.scalars().all()
    if req_data.skill_name != job_requirement.skill.name and any(req.skill.name == req_data.skill_name for req in req_list):
        raise HTTPException(status_code=400, detail=f"Requirement with {req_data.skill_name} name already exists")

    req_data_dict = req_data.dict(exclude_unset=True, exclude_none=True)
    update_model_instance(job_requirement, req_data_dict)

    await session.commit()
    await session.refresh(job_requirement)
    return job_requirement
