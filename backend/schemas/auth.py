from uuid import UUID

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    refresh_token: UUID
    session_id: int = Field(gt=0)


class RefreshToken(BaseModel):
    user_id: UUID
    token: UUID

    class Config:
        from_attributes = True
