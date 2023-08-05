import uuid

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, Field


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


# class Token(BaseModel):
#     id: uuid.UUID
#     token: dict
class Token(BaseModel):
    access_token: str
    token_type: str


# class UserRead(schemas.BaseUser[uuid.UUID]):
#     username: str
    # avatar: str
#
#
# class UserCreate(schemas.CreateUpdateDictModel):
#     username: str
#     email: EmailStr
#     password: str
#
#
# class UserUpdate(UserRead, schemas.BaseUserUpdate):
#     ...
