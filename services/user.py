from typing import Type
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from crud import CRUDUser
from models import UserDB
from schemas import UserRead


class UserService:
    @staticmethod
    async def get_user(user_id: UUID, session: AsyncSession) -> Type[UserDB] | None:
        crud_user = CRUDUser(UserDB, session)
        user = await crud_user.get(user_id)
        return user

    @staticmethod
    async def delete_user(user_id: UUID, session: AsyncSession) -> UserRead:
        crud_user = CRUDUser(UserDB, session)
        user = await crud_user.delete(user_id)
        return UserRead.model_validate(user)
