import uuid

from fastapi_users import schemas
from pydantic import EmailStr


# class User(BaseModel):
#     id: int
#     username: str
#
#     class Config:
#         from_attributes = True


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str

    # class Config:
    #     from_attributes = True


class UserCreate(schemas.CreateUpdateDictModel):
    username: str
    email: EmailStr
    password: str

    # class Config:
    #     from_attributes = True


class UserUpdate(UserRead, schemas.BaseUserUpdate):
    ...
