from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserRoleSchema(str, Enum):
    candidate = "candidate"
    recruiter = "recruiter"

class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(..., max_length=256)

class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    class Config:
        from_attributes = True

class UserViewSchema(UserUpdateSchema):
    id: Optional[int] = None



class UserSchema(UserBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=1, max_length=50)
    role: UserRoleSchema


class UserCredentialSchema(BaseModel):
    username: str
    password: str


class AccessTokenSchema(BaseModel):
    access_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenPairSchema(AccessTokenSchema, RefreshTokenSchema):
    pass
