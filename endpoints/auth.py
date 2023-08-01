from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, Form
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from config import GOOGLE_CLIENT_ID
from dependencies import get_session
from schemas import UserCreate, Token
from services import auth

router = APIRouter()


templates = Jinja2Templates(directory='templates')


@router.get('/')
async def google_auth(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


class Auth(BaseModel):
    credential: str
    g_csrf_token: str

# @router.post('/auth')
# async def test(credential: Annotated[str, Form()], g_csrf_token: Annotated[str, Form()], request: Request):
#     print(credential)
#     idinfo = id_token.verify_oauth2_token(credential, requests.Request(), GOOGLE_CLIENT_ID)
#     print(idinfo)
#     # print(jwt.decode(credential, key='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', algorithms=['base64']))
#     print(request)
#     return None


@router.post('/auth')
async def google_auth(credential: Annotated[str, Form()], g_csrf_token: Annotated[str, Form()], request: Request, session: AsyncSession = Depends(get_session)) -> Token:
    user_id, token = await auth.google_auth(
        token=credential,
        session=session,
    )
    return Token(id=user_id, token=token)
