from uuid import UUID

from pydantic import BaseModel

from backend.schemas import UserRead


class UploadVideo(BaseModel):
    title: str
    description: str | None
    file: str
    user: UUID


class GetVideo(UploadVideo):
    id: int
    like_count: int

    class Config:
        from_attributes = True


class GetVideoForHTML(GetVideo):
    user: UserRead


class CreateLikeOnVideo(BaseModel):
    video: int
    user: UUID

    class Config:
        from_attributes = True
