from datetime import datetime
from pydantic import BaseModel, conint
from typing import List, Optional
from enum import Enum

from src.candidates.schemas import SkillLevelSchema, SkillViewSchema

class JobRequirementSchema(BaseModel):
    skill_name: str
    minimal_level: SkillLevelSchema
    minimal_years_of_experience: int

class JobRequirementUpdateSchema(BaseModel):
    skill_name: Optional[str] = None
    minimal_level: Optional[SkillLevelSchema] = None
    minimal_years_of_experience: Optional[conint(gt=0)] = None

    class Config:
        from_attributes = True

class JobCreateSchema(BaseModel):
    title: str
    description: str
    requirements: List[JobRequirementSchema]


class JobRequirementViewSchema(BaseModel):
    id: int
    skill: SkillViewSchema
    minimal_level: SkillLevelSchema
    minimal_years_of_experience: int

    class Config:
        from_attributes = True 

class JobViewSchema(BaseModel):
    id: int
    recruiter_id: int
    title: str
    description: str
    created_at: datetime
    requirements: List[JobRequirementViewSchema]

    class Config:
        from_attributes = True





class JobUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True