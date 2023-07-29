import uuid

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str


class UserCreate(schemas.CreateUpdateDictModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(UserRead, schemas.BaseUserUpdate):
    ...
