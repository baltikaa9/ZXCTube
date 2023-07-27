import shutil
from typing import NewType, Type
from uuid import uuid4

import aiofiles

from fastapi import UploadFile, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserDB, VideoDB
from schemas import UploadVideo

VideoInfo = NewType('VideoInfo', dict)


async def save_video(
        user_id: int,
        file: UploadFile,
        title: str, description: str,
        background_tasks: BackgroundTasks,
        session: AsyncSession
) -> VideoInfo:
    file_name = _generate_file_name(user_id, file.content_type.split("/")[1])
    if file.content_type == 'video/mp4':
        background_tasks.add_task(write_video, path=file_name, video=file)
    else:
        raise HTTPException(status_code=418, detail='It isn\'t mp4')

    video = UploadVideo(title=title, description=description)
    new_video = VideoDB(
        title=video.title,
        description=video.description,
        file=file_name,
        user=user_id,
    )

    session.add(new_video)
    await session.commit()
    return VideoInfo({'file_name': file_name, 'user': user_id, 'info': video})


def _generate_file_name(user_id: int, file_format: str):
    return f'media/{user_id}_{uuid4()}.{file_format}'  # _{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}'


async def get_video(session: AsyncSession, video_id: int) -> Type[VideoDB] | None:
    video = await session.get(VideoDB, video_id)  # TODO: VideoCRUD
    return video


async def get_user(session: AsyncSession, user_id: int) -> Type[UserDB] | None:
    user = await session.get(UserDB, user_id)  # TODO: UserCRUD
    return user


def write_video(path: str, video: UploadFile):
    # async with aiofiles.open(path, 'wb') as file:
    #     data = await video.read()
    #     await file.write(data)
    with open(path, 'wb') as file:
        shutil.copyfileobj(video.file, file)
