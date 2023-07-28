from pydantic import BaseModel

from .user import User


class UploadVideo(BaseModel):
    title: str
    description: str | None
    # tags: list[str] = Field(default=None, max_items=3)


class GetListVideo(UploadVideo):
    id: int

    class Config:
        from_attributes = True


class GetVideo(GetListVideo):
    user: User
