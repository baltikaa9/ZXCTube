from datetime import timedelta, datetime
from uuid import UUID, uuid4

import jwt
from fastapi import HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from jwt import ExpiredSignatureError, PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from config import GOOGLE_CLIENT_ID, ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_JWT_SUBJECT, SECRET_KEY, ALGORITHM
from crud import CRUDRefreshToken
from models import RefreshTokenDB
from schemas import RefreshToken
from services import UserService


class AuthService:
    @staticmethod
    async def google_auth(
            token_id: str,
            session: AsyncSession,
    ) -> tuple[str, UUID]:
        try:
            id_info = id_token.verify_oauth2_token(token_id, requests.Request(), GOOGLE_CLIENT_ID,
                                                   clock_skew_in_seconds=10)
        except ValueError:
            raise HTTPException(status_code=403, detail='Bad credentials')
        user = await UserService.get_user_by_email(id_info.get('email'), session)
        if not user:
            user = await UserService.create_user(
                id_info.get('name'), id_info.get('email'), id_info.get('picture'), session
            )
        return Security.create_access_token(user.id), await Security.create_refresh_token(user.id, session)

    @staticmethod
    async def refresh_token(
            refresh_token: UUID,
            session: AsyncSession,
    ) -> tuple[str, UUID]:
        crud_token = CRUDRefreshToken(RefreshTokenDB, session)
        token = await crud_token.get(refresh_token)
        if not token:
            raise HTTPException(status_code=403, detail='Invalid token')
        await crud_token.delete_by_token(token.token)
        new_access_token = Security.create_access_token(token.user_id)
        new_refresh_token = await Security.create_refresh_token(token.user_id, session)
        return new_access_token, new_refresh_token

    @staticmethod
    async def logout(
            user_id: UUID,
            session: AsyncSession,
    ) -> UUID:
        crud_token = CRUDRefreshToken(RefreshTokenDB, session)
        return (await crud_token.delete_by_user(user_id)).token


class Security:
    @classmethod
    def create_access_token(cls, user_id: UUID) -> str:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return cls._create_access_token(
            data={'user_id': str(user_id)}, expires_delta=access_token_expires
        )

    @classmethod
    async def create_refresh_token(cls, user_id: UUID, session: AsyncSession) -> UUID:
        crud_token = CRUDRefreshToken(RefreshTokenDB, session)
        new_token = RefreshToken(user_id=user_id, token=uuid4())
        new_token = await crud_token.create(new_token)
        return new_token.token

    @staticmethod
    def _create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire, 'sub': ACCESS_TOKEN_JWT_SUBJECT})
        return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    @staticmethod
    async def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Unauthorized')
        except PyJWTError:
            raise HTTPException(status_code=403, detail='Bad credentials')
        return payload
