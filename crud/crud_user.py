from typing import Type
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models import UserDB


class CRUDUser:
    def __init__(self, model: Type[UserDB], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, user_id: UUID) -> Type[UserDB] | None:
        user = await self.session.get(self.model, user_id)
        return user
