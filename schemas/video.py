from uuid import UUID

from pydantic import BaseModel


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


class CreateLikeOnVideo(BaseModel):
    video: int
    user: UUID

    class Config:
        from_attributes = True
