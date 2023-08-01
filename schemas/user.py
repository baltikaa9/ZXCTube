import uuid

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, Field


class User(BaseModel):
    username: str
    email: EmailStr
    picture: str

    class Config:
        from_attributes = True


class UserCreate(User):
    # id: uuid.UUID
    # token: str
    ...


class UserUpdate(User):
    ...


class UserOut(BaseModel):
    id: uuid.UUID
    username: str


class Token(BaseModel):
    id: uuid.UUID
    token: dict


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
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
