from uuid import UUID

from pydantic import BaseModel

from schemas import UserRead


class FollowerCreate(BaseModel):
    user: UUID


class FollowerList(BaseModel):
    user: UserRead
    followers: list[UserRead]
