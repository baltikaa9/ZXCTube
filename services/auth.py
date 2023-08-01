from fastapi import HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from config import GOOGLE_CLIENT_ID
from schemas import UserCreate
from services import UserService
from services.tokenizator import create_token


async def google_auth(
        token: str,
        session: AsyncSession,
) -> tuple:
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(status_code=403, detail='Bad code')
    user_service = UserService()
    user = await user_service.create_user(
        idinfo.get('name'), idinfo.get('email'), idinfo.get('picture'), token, session
    )
    internal_token = create_token(str(user.id))
    return user.id, internal_token
