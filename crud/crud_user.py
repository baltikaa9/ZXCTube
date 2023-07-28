from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from models.user import UserDB


class CRUDUser:
    def __init__(self, session: AsyncSession):
        # self.model = model
        self.session = session

    async def create(self):
        ...

    async def get(self, user_id: int) -> Type[UserDB] | None:
        user = await self.session.get(UserDB, user_id)
        return user
