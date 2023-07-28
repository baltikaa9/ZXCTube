import uuid

from fastapi_users import schemas


# class User(BaseModel):
#     id: int
#     username: str
#
#     class Config:
#         from_attributes = True


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(UserRead, schemas.BaseUserUpdate):
    ...
