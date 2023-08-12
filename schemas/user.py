from uuid import UUID

from pydantic import EmailStr, BaseModel


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    picture: str

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: UUID
    username: str
    picture: str | None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    ...
