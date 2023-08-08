import uuid

from pydantic import EmailStr, BaseModel


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    picture: str

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    picture: str | None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    ...


class UserOut(BaseModel):
    id: uuid.UUID
    username: str


class Token(BaseModel):
    access_token: str
    refresh_token: uuid.UUID
    token_type: str
