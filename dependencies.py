import uuid
from typing import AsyncGenerator, cast, Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi_users import FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from auth import UserManager, auth_backend
from config import SECRET_KEY, ALGORITHM
from crud import CRUDUser
from db import async_session
from models import UserDB
from schemas import Token


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, UserDB)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


_fastapi_users = FastAPIUsers[UserDB, uuid.UUID](get_user_manager, [auth_backend])


# get_current_user = _fastapi_users.current_user(active=True)

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
    print(token)
    # access_token = token.token.get('access_token')
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except PyJWTError:
        raise HTTPException(status_code=403, detail='Bad credentials')

    user_id = payload.get('user_id')
    user_crud = CRUDUser(UserDB, session)
    user = await user_crud.get(user_id)
    return user
