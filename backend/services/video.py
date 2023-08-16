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
from config import VIDEO_STORAGE_PATH, PREVIEW_STORAGE_PATH


class VideoService:
    async def save_video(
            self,
            user: UserDB,
            file: UploadFile,
            title: str,
            description: str | None,
            preview: UploadFile | None,
            session: AsyncSession
    ) -> GetVideo:
        video_path = self._generate_video_path(user.id, file.content_type.split("/")[1])
        preview_path = None
        if file.content_type == 'video/mp4':
            await self._async_write_file(video_path, file)
        else:
            raise HTTPException(status_code=418, detail='Video isn\'t mp4')

        if preview:
            if preview.content_type.split('/')[0] != 'image':
                raise HTTPException(status_code=418, detail='Preview isn\'t image')
            else:
                preview_path = self._generate_preview_path(preview.filename)
                await self._async_write_file(preview_path, preview)

        video = UploadVideo(
            title=title,
            description=description,
            file=video_path,
            user=user.id,
            preview=preview_path.split('/')[-1] if preview else None,
        )
        crud_video = CRUDVideo(VideoDB, session)
        video = await crud_video.create(video)
        return GetVideo.model_validate(video)

    @staticmethod
    def _generate_video_path(user_id: UUID, file_format: str):
        return f'{VIDEO_STORAGE_PATH}/{user_id}_{uuid4()}.{file_format}'

    @staticmethod
    def _generate_preview_path(file_name: str):
        return f'{PREVIEW_STORAGE_PATH}/{uuid4()}_{file_name}'

    @staticmethod
    def _write_file(path: str, file: UploadFile):
        with open(path, 'wb') as file_obj:
            shutil.copyfileobj(file.file, file_obj)

    @staticmethod
    async def _async_write_file(path: str, file: UploadFile):
        async with aiofiles.open(path, 'wb') as file_obj:
            data = await file.read()
            await file_obj.write(data)

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
