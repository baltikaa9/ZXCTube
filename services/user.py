from typing import Type
from uuid import UUID

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from crud import CRUDUser
from exceptions import UserNotFoundException
from models import UserDB
from schemas import UserRead, UserCreate


class UserService:
    @staticmethod
    async def create_user(
            username: str,
            email: EmailStr,
            picture: str,
            session: AsyncSession,
    ) -> UserRead:
        user = UserCreate(username=username, email=email, picture=picture)
        crud_user = CRUDUser(UserDB, session)
        user = await crud_user.create(user)
        return UserRead.model_validate(user)

    @staticmethod
    async def get_user(user_id: UUID, session: AsyncSession) -> UserRead | None:
        crud_user = CRUDUser(UserDB, session)
        user = await crud_user.get(user_id)
        if user:
            return UserRead.model_validate(user)

    @staticmethod
    async def get_user_by_email(email: EmailStr, session: AsyncSession) -> UserRead | None:
        crud_user = CRUDUser(UserDB, session)
        user = await crud_user.get_by_email(email)
        if user:
            return UserRead.model_validate(user)

    @staticmethod
    async def delete_user(user_id: UUID, session: AsyncSession) -> UserRead | None:
        crud_user = CRUDUser(UserDB, session)
        user = await crud_user.delete(user_id)
        if user:
            return UserRead.model_validate(user)
