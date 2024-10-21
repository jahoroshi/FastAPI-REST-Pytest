from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from database import get_session
from src.auth.schemas import UserSchema, UserCreateSchema, TokenPairSchema, AccessTokenSchema, RefreshTokenSchema, \
    UserCredentialSchema
from src.auth.services import user_service, token_service

security = HTTPBasic()

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@router.post(
    '/registration',
    response_model=UserSchema,
    description="Registers a new user.",
    responses={
        201: {"description": "User successfully registered."},
        400: {"description": "Invalid data or user already exists."},
    }
)
async def add_user(user: UserCreateSchema, session=Depends(get_session)):
    return await user_service.create_user(user, session)


@router.post(
    '/token',
    response_model=TokenPairSchema,
    description="Obtains a pair of tokens using login and password.",
    responses={
        200: {"description": "Tokens generated successfully."},
        400: {"description": "Invalid user credentials."},
    }
)
async def get_token_pair(user_data: UserCredentialSchema, session=Depends(get_session)):
    credentials = HTTPBasicCredentials(username=user_data.username, password=user_data.password)
    user = await user_service.authenticate_user(credentials, session)
    return await token_service.create_token_pair(user_id=user.id)


@router.post(
    '/token/refresh',
    response_model=AccessTokenSchema,
    description="Refreshes the access token using a refresh token.",
    responses={
        200: {"description": "Token refreshed successfully."},
        401: {"description": "Invalid refresh token."},
    }
)
async def refresh_token(token: RefreshTokenSchema):
    return AccessTokenSchema(access_token=await token_service.refresh_access_token(token.refresh_token))
