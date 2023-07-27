from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    username: str


class UploadVideo(BaseModel):
    title: str
    description: str
    # tags: list[str] = Field(default=None, max_items=3)


class GetVideo(BaseModel):
    user: User
    video: UploadVideo


class Message(BaseModel):
    message: str
