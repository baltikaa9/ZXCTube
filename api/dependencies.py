from typing import AsyncGenerator, cast, Any

from fastapi import Depends, HTTPException
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from crud import CRUDUser
from db import async_session
from models import UserDB
from services import Security


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class OAuth2ClientCredentials(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: str | None = None,
            scopes: dict[str, str] | None = None,
            description: str | None = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(
            clientCredentials=cast(Any, {'tokenUrl': tokenUrl, 'scopes': scopes})
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    def __call__(self, request: Request):
        authorization = request.headers.get('Authorization')
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != 'bearer':
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail='Not authenticated',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            else:
                return None
        return param


oauth2_schema = OAuth2ClientCredentials(tokenUrl='/api/auth/token')


async def get_current_user(
        token: str | None = Depends(oauth2_schema),
        session: AsyncSession = Depends(get_session),
) -> UserDB | None:
    payload = await Security.decode_token(token)
    user_id = payload.get('user_id')
    user_crud = CRUDUser(UserDB, session)
    user = await user_crud.get(user_id)
    return user
