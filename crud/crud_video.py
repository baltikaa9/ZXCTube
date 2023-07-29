from uuid import UUID

from sqlalchemy import select

from crud import CRUDBase
from models import VideoDB
from schemas import UploadVideo


class CRUDVideo(CRUDBase[VideoDB, UploadVideo]):
    async def get_by_user(self, user_id: UUID) -> list[VideoDB]:
        query = select(self.model).where(self.model.user == user_id)
        videos = await self.session.execute(query)
        return [video[0] for video in videos.all()]
