from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import CandidateProfile, Skill, CandidateSkill
from src.candidates.schemas import CandidateSkillCreateSchema, CandidateSkillUpdateSchema
from src.tools.database import get_object
from src.tools.profile import check_role


async def add_candidate_skill_service(skill_data: CandidateSkillCreateSchema, current_user, session: AsyncSession):
    await check_role(current_user, 'candidate')

    profile = await get_object(CandidateProfile, CandidateProfile.user_id == current_user.id, session)
    skill = await get_object(Skill, Skill.name == skill_data.skill_name, session)

    user_skills = profile.skills
    if any(skill.skill.name == skill_data.skill_name for skill in user_skills):
        raise HTTPException(status_code=400, detail="The skill already exist for this user.")

    if skill is None:
        skill = Skill(name=skill_data.skill_name)
        session.add(skill)
        await session.commit()
        await session.refresh(skill)

    candidate_skill = CandidateSkill(
        candidate_id=profile.user_id,
        skill_id=skill.id,
        level=skill_data.level,
        years_of_experience=skill_data.years_of_experience,
        last_used_year=skill_data.last_used_year,
    )

    session.add(candidate_skill)
    await session.commit()
    await session.refresh(candidate_skill)
    return candidate_skill


async def update_candidate_skill_service(skill_data: CandidateSkillUpdateSchema, skill_id: int, current_user,
                                         session: AsyncSession):
    await check_role(current_user, 'candidate')
    query = select(CandidateSkill).join(CandidateSkill.candidate).where(CandidateSkill.id == skill_id,
                                                                        CandidateProfile.user_id == current_user.id)
    result = await session.execute(query)
    candidate_skill = result.scalar_one_or_none()

    if candidate_skill is None:
        raise HTTPException(status_code=404, detail='Skill not found')

    skill_data_dict = skill_data.dict(exclude_unset=True, exclude_none=True)

    if candidate_skill.skill.name != skill_data.skill_name and skill_data.skill_name is not None:
        skill = await get_object(Skill, Skill.name == skill_data.skill_name, session)

        if skill is None:
            skill = Skill(name=skill_data.skill_name)
            session.add(skill)
            await session.commit()
            await session.refresh(skill)

        candidate_skill.skill_id = skill.id
        await session.flush()

        candidate_profile = candidate_skill.candidate
        user_skills = candidate_profile.skills
        if any(skill.skill.name == skill_data.skill_name for skill in user_skills):
            raise HTTPException(status_code=400, detail=f"Skill with {skill_data.skill_name} name already exists for this user.")

    for key, value in skill_data_dict.items():
        if key != 'skill_name':
            setattr(candidate_skill, key, value)

    await session.commit()
    await session.refresh(candidate_skill)

    return candidate_skill


async def delete_candidate_skill_service(skill_id: int, current_user, session: AsyncSession):
    query = select(CandidateSkill).join(CandidateSkill.candidate).where(CandidateSkill.id == skill_id,
                                                                        CandidateProfile.user_id == current_user.id)
    result = await session.execute(query)
    skill = result.scalar_one_or_none()

    if skill is None:
        raise HTTPException(status_code=404, detail='Skill not found')

    await session.delete(skill)
    await session.commit()

    return Response(status_code=204)
