from typing import overload
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select, delete

from crud import CRUDBase
from models import RefreshTokenDB
from schemas import RefreshToken


class CRUDRefreshToken(CRUDBase[RefreshTokenDB, RefreshToken]):
    async def get_by_token(self, token: UUID) -> RefreshTokenDB | None:
        query = select(self.model).where(self.model.token == token)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()

    async def delete_by_user(self, user_id: UUID) -> list[RefreshTokenDB] | None:
        query = delete(self.model) \
            .where(self.model.user_id == user_id) \
            .returning(self.model)
        refresh_token = await self.session.execute(query)
        await self.session.commit()
        return [refresh_token[0] for refresh_token in refresh_token.all()]

    async def delete_by_token(self, token: UUID) -> RefreshTokenDB | None:
        query = delete(self.model) \
            .where(self.model.token == token) \
            .returning(self.model)
        refresh_token = await self.session.execute(query)
        await self.session.commit()
        return refresh_token.scalar_one_or_none()
