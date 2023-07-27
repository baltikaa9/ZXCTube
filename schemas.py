from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    username: str


class UploadVideo(BaseModel):
    title: str
    description: str
    # tags: list[str] = Field(default=None, max_items=3)


class GetListVideo(UploadVideo):
    id: int

    class Config:
        from_attributes = True


class GetVideo(GetListVideo):
    user: User


class Message(BaseModel):
    message: str
