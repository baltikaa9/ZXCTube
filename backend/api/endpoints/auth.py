from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from backend.api.dependencies import get_session, get_current_user
from backend.schemas import Token
from backend.services import AuthService

router = APIRouter(prefix='/auth', tags=['Auth'])

templates = Jinja2Templates(directory='frontend/templates')


@router.post('/login')
async def google_auth(
        credential: Annotated[str, Body()],
        session: AsyncSession = Depends(get_session),
        service: AuthService = Depends(),
) -> Token:
    return await service.google_auth(
        token_id=credential,
        session=session,
    )


@router.post('/refresh')
async def refresh(
        refresh_token: UUID,
        session: AsyncSession = Depends(get_session),
        service: AuthService = Depends(),
) -> Token:
    return await service.refresh_token(
        refresh_token=refresh_token,
        session=session,
    )


@router.post('/logout', dependencies=[Depends(get_current_user)])
async def logout(
        session_id: int,
        session: AsyncSession = Depends(get_session),
        service: AuthService = Depends(),
) -> dict:
    await service.logout(session_id, session)
    return {'Success': True}
