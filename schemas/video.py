from pydantic import BaseModel

from schemas import UserRead


class UploadVideo(BaseModel):
    title: str
    description: str | None


class GetListVideo(UploadVideo):
    id: int

    class Config:
        from_attributes = True


class GetVideo(GetListVideo):
    user: UserRead
