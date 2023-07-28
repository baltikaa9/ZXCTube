from typing import Type
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models.video import VideoDB
from schemas.video import UploadVideo


class CRUDVideo:
    def __init__(self, model: Type[VideoDB], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, video: UploadVideo, file_name: str, user_id: int) -> VideoDB:
        new_video = self.model(
            title=video.title,
            description=video.description,
            file=file_name,
            user=user_id,
        )
        self.session.add(new_video)
        await self.session.commit()
        return new_video

    async def get(self, video_id: int) -> Type[VideoDB] | None:
        video = await self.session.get(self.model, video_id)
        return video

    async def get_by_user(self, user_id: UUID) -> list[VideoDB]:
        query = select(self.model).where(self.model.user == user_id)
        videos = await self.session.execute(query)
        return [video[0] for video in videos.all()]

    async def update(self):
        ...

    async def delete(self, video_id: int) -> Type[VideoDB] | None:
        statement = delete(self.model).where(self.model.id == video_id).returning(self.model)
        video = await self.session.execute(statement)
        # print(video.all())
        await self.session.commit()
        try:
            return video.scalar_one()
        except NoResultFound:
            return
