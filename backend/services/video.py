import os
import shutil
from pathlib import Path
from typing import Generator, IO
from uuid import UUID, uuid4

import aiofiles
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks
from starlette.requests import Request

from backend.crud import CRUDVideo, CRUDVideoLike
from backend.exceptions import VideoNotFoundException
from backend.models import UserDB, VideoDB, VideoLikeDB
from backend.schemas import UploadVideo, GetVideo, CreateLikeOnVideo


class VideoService:
    async def save_video(
            self,
            user: UserDB,
            file: UploadFile,
            title: str,
            description: str | None,
            background_tasks: BackgroundTasks,
            session: AsyncSession
    ) -> GetVideo:
        file_name = self._generate_file_name(user.id, file.content_type.split("/")[1])
        if file.content_type == 'video/mp4':
            # background_tasks.add_task(write_video, path=file_name, video=file)
            await self._async_write_video(file_name, file)
        else:
            raise HTTPException(status_code=418, detail='It isn\'t mp4')

        video = UploadVideo(title=title, description=description, file=file_name, user=user.id)
        crud_video = CRUDVideo(VideoDB, session)
        video = await crud_video.create(video)
        return GetVideo.model_validate(video)

    @staticmethod
    def _generate_file_name(user_id: UUID, file_format: str):
        return f'media/{user_id}_{uuid4()}.{file_format}'

    @staticmethod
    def _write_video(path: str, video: UploadFile):
        with open(path, 'wb') as file:
            shutil.copyfileobj(video.file, file)

    @staticmethod
    async def _async_write_video(path: str, video: UploadFile):
        async with aiofiles.open(path, 'wb') as file:
            data = await video.read()
            await file.write(data)

    @staticmethod
    async def delete_video(video_id, session: AsyncSession) -> GetVideo | None:
        crud_video = CRUDVideo(VideoDB, session)
        video = await crud_video.delete(video_id)
        if video:
            file_name = video.file
            os.remove(file_name)
            return GetVideo.model_validate(video)

    @staticmethod
    async def get_video(video_id: int, session: AsyncSession) -> GetVideo | None:
        crud_video = CRUDVideo(VideoDB, session)
        video = await crud_video.get(video_id)
        if video:
            return GetVideo.model_validate(video)

    @staticmethod
    async def get_videos_by_user(user_id: UUID, session: AsyncSession) -> list[GetVideo]:
        crud_video = CRUDVideo(VideoDB, session)
        videos = await crud_video.get_all(user_id)
        return [GetVideo.model_validate(video) for video in videos]

    @staticmethod
    async def get_all_videos(session: AsyncSession) -> list[GetVideo]:
        crud_video = CRUDVideo(VideoDB, session)
        videos = await crud_video.get_all()
        return [GetVideo.model_validate(video) for video in videos]

    @staticmethod
    def _ranged(
            file: IO[bytes],
            start: int = 0,
            end: int = None,
            block_size: int = 8192,
    ) -> Generator[bytes, None, None]:
        consumed = 0

        file.seek(start)
        while True:
            data_length = min(block_size, end - start - consumed) if end else block_size
            if data_length <= 0:
                break
            data = file.read(data_length)
            if not data:
                break
            consumed += data_length
            yield data

        if hasattr(file, 'close'):
            file.close()

    async def open_file(self, video_id: int, request: Request, session: AsyncSession):
        video = await self.get_video(video_id, session)
        if not video:
            raise VideoNotFoundException()

        path = Path(video.file)
        file = path.open('rb')

        file_size = path.stat().st_size

        content_length = file_size
        status_code = 200
        headers = {}
        content_range = request.headers.get('range')

        if content_range:
            content_range = content_range.strip().lower()
            content_ranges = content_range.split('=')[-1]
            range_start, range_end, *_ = map(str.strip, content_ranges.split('-'))
            range_start = int(range_start) if range_start else 0
            range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
            content_length = range_end - range_start + 1
            file = self._ranged(file, start=range_start, end=range_end + 1)
            status_code = 206
            headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

        return file, status_code, content_length, headers

    @staticmethod
    async def add_or_delete_like(
            video_id: int,
            session: AsyncSession,
            current_user: UserDB,
    ) -> GetVideo:
        crud_video = CRUDVideo(VideoDB, session)
        crud_like = CRUDVideoLike(VideoLikeDB, session)
        like = CreateLikeOnVideo(video=video_id, user=current_user.id)
        like_db = await crud_like.get_like(like)
        if like_db:
            video = await crud_video.delete_like(video_id)
            if not video:
                raise VideoNotFoundException()
            await crud_like.delete(like_db.id)
        else:
            video = await crud_video.add_like(video_id)
            if not video:
                raise VideoNotFoundException()
            await crud_like.create(like)
        return GetVideo.model_validate(video)
