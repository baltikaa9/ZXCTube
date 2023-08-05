from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.ext.asyncio import AsyncSession

from config import GOOGLE_CLIENT_ID, ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_JWT_SUBJECT, SECRET_KEY, ALGORITHM
from exceptions import UserNotFoundException
from services import UserService


class AuthService:
    @staticmethod
    async def google_auth(
            token_id: str,
            session: AsyncSession,
    ) -> str:
        try:
            id_info = id_token.verify_oauth2_token(token_id, requests.Request(), GOOGLE_CLIENT_ID)
        except ValueError:
            raise HTTPException(status_code=403, detail='Bad code')
        user_service = UserService()
        try:
            user = await user_service.get_user_by_email(id_info.get('email'), session)
        except UserNotFoundException:
            user = await user_service.create_user(
                id_info.get('name'), id_info.get('email'), id_info.get('picture'), session
            )
        return Tokenizer.create_token(str(user.id))


class Tokenizer:
    @classmethod
    def create_token(cls, user_id: str) -> str:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return cls._create_access_token(
            data={'user_id': user_id}, expires_delta=access_token_expires
        )

    @staticmethod
    def _create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire, 'sub': ACCESS_TOKEN_JWT_SUBJECT})
        return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

