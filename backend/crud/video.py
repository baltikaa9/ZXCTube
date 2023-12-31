from uuid import UUID

from sqlalchemy import select, update

from backend.crud import CRUDBase
from backend.models import VideoDB, VideoLikeDB
from backend.schemas import UploadVideo, CreateLikeOnVideo


class CRUDVideo(CRUDBase[VideoDB, UploadVideo]):
    async def get_all(self, user_id: UUID | None = None) -> list[VideoDB]:
        if user_id:
            query = select(self.model).where(self.model.user == user_id)
        else:
            query = select(self.model)
        videos = await self.session.execute(query)
        return [video[0] for video in videos.all()]

    async def add_like(self, video_id: int) -> VideoDB:
        video = await self.get(video_id)
        query = update(self.model).where(self.model.id == video_id).values(like_count=self.model.like_count + 1)
        await self.session.execute(query)
        await self.session.commit()
        return video

    async def delete_like(self, video_id: int) -> VideoDB:
        video = await self.get(video_id)
        query = update(self.model).where(self.model.id == video_id).values(like_count=self.model.like_count - 1)
        await self.session.execute(query)
        await self.session.commit()
        return video


class CRUDVideoLike(CRUDBase[VideoLikeDB, CreateLikeOnVideo]):
    async def get_like(self, like: CreateLikeOnVideo) -> VideoLikeDB | None:
        query = select(self.model).where((self.model.video == like.video) & (self.model.user == like.user))
        like = await self.session.execute(query)
        return like.scalar_one_or_none()
