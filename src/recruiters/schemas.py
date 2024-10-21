from pydantic import BaseModel
from typing import List, Optional

from src.auth.schemas import UserViewSchema, UserUpdateSchema


class RecruiterCreateSchema(BaseModel):
    company_name: str
    position: str

class RecruiterViewSchema(BaseModel):
    company_name: Optional[str] = None
    # jobs: List['Jobs'] = []

    class Config:
        from_attributes = True

class UserRecruiterViewSchema(BaseModel):
    user: UserViewSchema
    recruiter_profile: RecruiterViewSchema

class RecruiterUpdateSchema(BaseModel):
    company_name: Optional[str] = None

    class Config:
        from_attributes = True

class UserRecruiterUpdateSchema(BaseModel):
    user: UserUpdateSchema
    recruiter_profile: RecruiterUpdateSchema