import enum
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from src.candidates.schemas import SkillLevelSchema, CandidateStatus


class UserRole(enum.Enum):
    candidate = 'candidate'
    recruiter = 'recruiter'


class SkillLevel(enum.Enum):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(150))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))

    candidate_profile: Mapped['CandidateProfile'] = relationship('CandidateProfile',
                                                                 back_populates='user',
                                                                 lazy="selectin",
                                                                 cascade='all, delete-orphan')

    recruiter_profile: Mapped['RecruiterProfile'] = relationship('RecruiterProfile',
                                                                 back_populates='user',
                                                                 lazy="selectin",
                                                                 cascade='all, delete-orphan')



class CandidateProfile(Base):
    __tablename__ = 'candidate_profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    # status: Mapped[CandidateStatus] = mapped_column(Enum(CandidateStatus))

    user: Mapped['User'] = relationship('User', back_populates='candidate_profile')
    skills: Mapped[List['CandidateSkill']] = relationship('CandidateSkill', back_populates='candidate', lazy="selectin",
                                                          cascade='all, delete-orphan')


class RecruiterProfile(Base):
    __tablename__ = 'recruiter_profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    user: Mapped['User'] = relationship('User', back_populates='recruiter_profile', lazy="selectin")
    jobs: Mapped[List['Job']] = relationship('Job', back_populates='recruiter', cascade='all, delete-orphan')


class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class CandidateSkill(Base):
    __tablename__ = 'candidate_skills'

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey('candidate_profiles.id'))
    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'))
    level: Mapped[SkillLevelSchema] = mapped_column(Enum(SkillLevelSchema))
    years_of_experience: Mapped[int] = mapped_column(Integer)
    last_used_year: Mapped[int] = mapped_column(Integer)

    candidate = relationship('CandidateProfile', back_populates='skills')
    skill = relationship('Skill', lazy="selectin")


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[int] = mapped_column(primary_key=True)
    recruiter_id: Mapped[int] = mapped_column(ForeignKey('recruiter_profiles.id'))
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    recruiter = relationship('RecruiterProfile', back_populates='jobs', lazy="selectin")
    requirements = relationship('JobRequirement', back_populates='job', cascade='all, delete-orphan', lazy="selectin")


class JobRequirement(Base):
    __tablename__ = 'job_requirements'

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey('jobs.id'))
    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'))
    minimal_level: Mapped[SkillLevelSchema] = mapped_column(Enum(SkillLevelSchema))
    minimal_years_of_experience: Mapped[int] = mapped_column(Integer)

    job = relationship('Job', back_populates='requirements', lazy="selectin")
    skill = relationship('Skill', lazy="selectin")

    __table_args__ = (
        UniqueConstraint(
            'job_id', 'skill_id', 'minimal_level', 'minimal_years_of_experience',
            name='uix_job_skill_level_experience'
        ),
    )

# class Task(Base):
#     __tablename__ = 'tasks'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     task_info: Mapped[str] = mapped_column(String(256))
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
#     updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#     datetime_to_do: Mapped[datetime] = mapped_column(DateTime(timezone=True))
#     user_id: Mapped['int'] = mapped_column(ForeignKey('users.id'))
#
#     user: Mapped['User'] = relationship('User', back_populates='tasks')
