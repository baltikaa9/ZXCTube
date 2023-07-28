import os
import shutil
from pathlib import Path
from typing import NewType, Type, IO, Generator
from uuid import uuid4, UUID

import aiofiles

from fastapi import UploadFile, BackgroundTasks, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from crud.crud_user import CRUDUser
from crud.crud_video import CRUDVideo
from db.session import get_session
from models import UserDB, FollowerDB
from models import VideoDB
from schemas import UploadVideo, GetListVideo, UserRead
from schemas.follower import FollowerList

VideoInfo = NewType('VideoInfo', dict)


async def save_video(
        user_id: int | UUID,
        file: UploadFile,
        title: str,
        description: str | None,
        background_tasks: BackgroundTasks,
        session: AsyncSession
) -> VideoDB:
    file_name = _generate_file_name(user_id, file.content_type.split("/")[1])
    if file.content_type == 'video/mp4':
        # background_tasks.add_task(write_video, path=file_name, video=file)
        await async_write_video(file_name, file)
    else:
        raise HTTPException(status_code=418, detail='It isn\'t mp4')

    video = UploadVideo(title=title, description=description)
    crud_video = CRUDVideo(VideoDB, session)
    video = await crud_video.create(video, file_name, user_id)
    # return VideoInfo({'file_name': file_name, 'user': user_id, 'info': video})
    return video


async def delete_video(video_id, session: AsyncSession) -> Type[VideoDB]:
    crud_video = CRUDVideo(VideoDB, session)
    video = await crud_video.delete(video_id)
    if not video:
        raise HTTPException(status_code=404, detail='Video not found')
    file_name = video.file
    os.remove(file_name)
    # while True:
    #     try:
    #
    #         break
    #     except PermissionError:
    #         ...
    return video


def _generate_file_name(user_id: int, file_format: str):
    return f'media/{user_id}_{uuid4()}.{file_format}'  # _{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}'


async def get_video(video_id: int, session: AsyncSession) -> Type[VideoDB] | None:
    crud_video = CRUDVideo(VideoDB, session)
    video = await crud_video.get(video_id)
    return video


async def get_videos_by_user(user_id: UUID, session: AsyncSession) -> list[GetListVideo]:
    crud_video = CRUDVideo(VideoDB, session)
    videos = await crud_video.get_by_user(user_id)
    return [GetListVideo.model_validate(video) for video in videos]


async def get_user(user_id: UUID, session: AsyncSession) -> Type[UserDB] | None:
    crud_user = CRUDUser(session)
    user = await crud_user.get(user_id)
    return user


def write_video(path: str, video: UploadFile):
    with open(path, 'wb') as file:
        shutil.copyfileobj(video.file, file)


async def async_write_video(path: str, video: UploadFile):
    async with aiofiles.open(path, 'wb') as file:
        data = await video.read()
        await file.write(data)


def ranged(
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


async def open_file(video_id: int, request: Request, session: AsyncSession):
    video = await get_video(video_id, session)
    if not video:
        raise HTTPException(status_code=404, detail='Video not found')

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
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, headers


async def get_followers_by_user(
    user: UUID,
    session: AsyncSession = Depends(get_session),
) -> FollowerList:
    query = select(FollowerDB).where(FollowerDB.user == user)
    followers = await session.execute(query)
    followers = followers.scalars().all()
    follower_list = FollowerList(user=await session.get(UserDB, user), followers=[])
    for follower in followers:
        subscriber = await session.get(UserDB, follower.subscriber)
        follower_list.followers.append(UserRead.model_validate(subscriber))
    return follower_list
