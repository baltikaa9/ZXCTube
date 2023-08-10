from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: UUID


class RefreshToken(BaseModel):
    user_id: UUID
    token: UUID

    class Config:
        from_attributes = True
