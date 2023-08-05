from typing import AsyncGenerator, cast, Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2PasswordBearer, OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from config import SECRET_KEY, ALGORITHM
from crud import CRUDUser
from db import async_session
from models import UserDB


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session







# oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/token')


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
            clientCredentials=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes})
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> str | None:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_schema = OAuth2(flows=OAuthFlows(
    clientCredentials=cast(Any, {"tokenUrl": '/auth/token'})
))


async def get_current_user(
        token: str = Depends(oauth2_schema),
        session: AsyncSession = Depends(get_session),
) -> None:
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except PyJWTError:
        raise HTTPException(status_code=403, detail='Bad credentials')

    user_id = payload.get('user_id')
    user_crud = CRUDUser(UserDB, session)
    user = await user_crud.get(user_id)
    return user
