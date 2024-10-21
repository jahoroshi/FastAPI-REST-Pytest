from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Job, CandidateProfile
from src.candidates.schemas import UserCandidateViewSchema, CandidateViewSchema, CandidateSkillViewSchema
from src.jobs.schemas import JobViewSchema
from src.tools.database import get_object
from src.tools.profile import check_role


async def get_matching_candidates_service(job_id: int, current_user, session: AsyncSession):
    job = await get_object(Job, Job.id == job_id, session)
    if not job or job.recruiter != current_user.recruiter_profile:
        raise HTTPException(status_code=404, detail="Job not found")
    requirements = job.requirements

    query = (
        select(CandidateProfile)
        .options(
            selectinload(CandidateProfile.user),
            selectinload(CandidateProfile.skills)
        )
    )
    result = await session.execute(query)
    candidates = result.scalars().all()
    candidate_scores = []

    current_year = datetime.now().year

    for candidate in candidates:
        score, match = 0, True
        candidate_skills = {cs.skill_id: cs for cs in candidate.skills}

        for req_skill in requirements:
            candidate_skill = candidate_skills.get(req_skill.skill_id)
            if not candidate_skill:
                match = False
                break

            levels = ["beginner", "intermediate", "advanced"]
            candidate_level_index = levels.index(candidate_skill.level.value)
            required_level_index = levels.index(req_skill.minimal_level.value)

            if candidate_level_index < required_level_index:
                score -= (required_level_index - candidate_level_index) * 0.5
            else:
                score += (candidate_level_index - required_level_index) * 0.5

            score += 1
            experience_diff = candidate_skill.years_of_experience - req_skill.minimal_years_of_experience
            score += max(0, experience_diff) * 0.1

            years_since_last_used = current_year - candidate_skill.last_used_year
            if years_since_last_used <= 1:
                score += 1
            elif 1 < years_since_last_used <= 3:
                score += 0.5
            else:
                score -= 0.5

        if match:
            candidate_scores.append((candidate, score))

    candidate_scores.sort(key=lambda x: x[1], reverse=True)

    result = []
    for candidate, score in candidate_scores:
        sorted_skills = sorted(
            candidate.skills,
            key=lambda skill: (
                -levels.index(skill.level.value),
                -skill.years_of_experience,
                abs(current_year - skill.last_used_year)
            )
        )

        candidate_profile_data = CandidateViewSchema.from_orm(candidate)
        candidate_profile_data.skills = [
            CandidateSkillViewSchema.from_orm(skill) for skill in sorted_skills
        ]

        result.append(
            UserCandidateViewSchema(
                user=candidate.user,
                candidate_profile=candidate_profile_data
            )
        )

    return result


async def get_matching_jobs_service(current_user, session: AsyncSession):
    await check_role(current_user, 'candidate')

    candidate_profile = current_user.candidate_profile
    if not candidate_profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found")

    candidate_skills = {cs.skill_id: cs for cs in candidate_profile.skills}

    query = (
        select(Job)
        .options(selectinload(Job.requirements))
    )
    result = await session.execute(query)
    jobs = result.scalars().all()

    job_scores = []

    for job in jobs:
        score, match = 0, True

        for req_skill in job.requirements:
            candidate_skill = candidate_skills.get(req_skill.skill_id)
            if not candidate_skill:
                match = False
                break

            levels = ["beginner", "intermediate", "advanced"]
            candidate_level_index = levels.index(candidate_skill.level.value)
            required_level_index = levels.index(req_skill.minimal_level.value)

            if candidate_level_index < required_level_index:
                score -= (required_level_index - candidate_level_index) * 0.5
            else:
                score += (candidate_level_index - required_level_index) * 0.5

            score += 1
            experience_diff = candidate_skill.years_of_experience - req_skill.minimal_years_of_experience
            score += max(0, experience_diff) * 0.1

        if match:
            job_scores.append((job, score))

    job_scores.sort(key=lambda x: x[1], reverse=True)

    return [job for job, score in job_scores]
