from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, field_validator
from pydantic import conint

from src.auth.schemas import UserUpdateSchema, UserViewSchema


class SkillLevelSchema(str, Enum):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'


class CandidateStatus(str, Enum):
    open_to_offers = 'open_to_offers'
    actively_applying = 'actively_applying'
    interviewing = 'interviewing'


class CandidateCreateSchema(BaseModel):
    ...


class CandidateBaseSchema(BaseModel):
    id: int
    user_id: int
    skills: List['CandidateSkillViewSchema'] = []

    class Config:
        from_attributes = True


class CandidateViewSchema(BaseModel):
    skills: List['CandidateSkillViewSchema'] = []
    # status: CandidateStatus

    class Config:
        from_attributes = True


class UserCandidateViewSchema(BaseModel):
    user: UserViewSchema
    candidate_profile: CandidateViewSchema


class CandidateProfileUpdateSchema(BaseModel):
    # status: CandidateStatus

    class Config:
        from_attributes = True


class UserCandidateUpdateSchema(BaseModel):
    user: UserUpdateSchema
    candidate_profile: CandidateProfileUpdateSchema


class CandidateSkillCreateSchema(BaseModel):
    skill_name: str
    level: SkillLevelSchema
    years_of_experience: conint(ge=0)
    last_used_year: conint(gt=0)

    @field_validator('last_used_year')
    def validate_last_used_year(cls, value):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError('Last used year cannot be in the future')
        return value


class CandidateSkillUpdateSchema(BaseModel):
    skill_name: Optional[str] = None
    level: Optional[SkillLevelSchema] = None
    years_of_experience: Optional[conint(gt=0)] = None
    last_used_year: Optional[conint(gt=0)] = None

    @field_validator('last_used_year')
    def validate_last_used_year(cls, value):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError('Last used year cannot be in the future')
        return value


class CandidateSkillViewSchema(BaseModel):
    id: int
    skill: 'SkillViewSchema'
    level: SkillLevelSchema
    years_of_experience: int
    last_used_year: int

    class Config:
        from_attributes = True


class SkillViewSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


UserCandidateViewSchema.update_forward_refs()
CandidateSkillViewSchema.update_forward_refs()
