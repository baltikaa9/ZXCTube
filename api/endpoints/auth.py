from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from api.dependencies import get_session, get_current_user_from_headers
from models import UserDB
from schemas import Token
from services import AuthService

router = APIRouter(prefix='/auth', tags=['Auth'])

templates = Jinja2Templates(directory='frontend/templates')


@router.post('/login')
async def google_auth(
        credential: Annotated[str, Body()],
        session: AsyncSession = Depends(get_session),
        service: AuthService = Depends(),
) -> Token:
    access_token, refresh_token = await service.google_auth(
        token_id=credential,
        session=session,
    )
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post('/refresh')
async def refresh(
        refresh_token: UUID,
        session: AsyncSession = Depends(get_session),
        service: AuthService = Depends(),
) -> Token:
    access_token, refresh_token = await service.refresh_token(
        refresh_token=refresh_token,
        session=session,
    )
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post('/logout')  # TODO: сделать logout не из всех сессий, а только из текущей (удалять из базы только токены данной сессии, а не все), а то это баг.
async def logout(
        current_user: UserDB = Depends(get_current_user_from_headers),
        session: AsyncSession = Depends(get_session),
        service: AuthService = Depends(),
) -> dict:
    await service.logout(current_user.id, session)
    return {'Success': True}
