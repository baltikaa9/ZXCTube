from pydantic import EmailStr
from sqlalchemy import select

from backend.crud import CRUDBase
from backend.models import UserDB
from backend.schemas import UserCreate


class CRUDUser(CRUDBase[UserDB, UserCreate]):
    async def get_by_email(self, email: EmailStr) -> UserDB | None:
        query = select(self.model).where(self.model.email == email)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
