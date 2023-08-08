from uuid import UUID

from pydantic import BaseModel


class RefreshToken(BaseModel):
    user_id: UUID
    token: UUID

    class Config:
        from_attributes = True
