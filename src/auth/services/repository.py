from typing import Sequence
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, CandidateProfile, RecruiterProfile


class UserRepository:

    @staticmethod
    async def add_user(user: User, session: AsyncSession) -> User:
        try:
            async with session.begin():
                session.add(user)
                await session.flush()
                if user.role.value == 'candidate':
                    candidate_profile = CandidateProfile(user_id=user.id)
                    session.add(candidate_profile)
                elif user.role.value == 'recruiter':
                    recruiter_profile = RecruiterProfile(user_id=user.id)
                    session.add(recruiter_profile)
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=f"Error with creating user. {e}")
        return user

    @staticmethod
    async def get_user_by_username(username: str, session: AsyncSession) -> User:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()