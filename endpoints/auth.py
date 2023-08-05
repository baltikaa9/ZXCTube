from typing import Annotated

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from dependencies import get_session
from schemas import Token
from services import AuthService

router = APIRouter(prefix='/auth')

templates = Jinja2Templates(directory='templates')


@router.get('/')
async def google_auth(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


@router.post('/token')
async def google_auth(
        credential: Annotated[str, Form()],
        session: AsyncSession = Depends(get_session),
        service: AuthService = Depends(),
) -> Token:
    token = await service.google_auth(
        token_id=credential,
        session=session,
    )
    return Token(access_token=token, token_type='bearer')
