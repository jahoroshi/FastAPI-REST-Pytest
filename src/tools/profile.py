from fastapi import HTTPException

from models import User


async def check_role(current_user: User, role: str):
    if current_user.role.value != role:
        raise HTTPException(status_code=400, detail=f"The profile must have {role} status.")