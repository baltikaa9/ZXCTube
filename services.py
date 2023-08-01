import os
import shutil
from pathlib import Path
from typing import Type, IO, Generator
from uuid import uuid4, UUID

import aiofiles
from fastapi import UploadFile, BackgroundTasks, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from crud import CRUDSubscription, CRUDVideoLike
from crud import CRUDUser
from crud import CRUDVideo
from dependencies import get_session
from exceptions import VideoNotFoundException, UserNotFoundException
from models import UserDB, SubscriptionDB, VideoLikeDB
from models import VideoDB
from schemas import SubscriberList, SubscriptionList, SubscriberCreate, CreateLikeOnVideo
from schemas import UploadVideo, GetListVideo, UserRead, GetVideo


async def save_video(
        user: UserDB,
        file: UploadFile,
        title: str,
        description: str | None,
        background_tasks: BackgroundTasks,
        session: AsyncSession
) -> GetVideo:
    file_name = _generate_file_name(user.id, file.content_type.split("/")[1])
    if file.content_type == 'video/mp4':
        # background_tasks.add_task(write_video, path=file_name, video=file)
        await async_write_video(file_name, file)
    else:
        raise HTTPException(status_code=418, detail='It isn\'t mp4')

    video = UploadVideo(title=title, description=description, file=file_name, user=user.id)
    crud_video = CRUDVideo(VideoDB, session)
    video = await crud_video.create(video)
    video.user = UserRead.model_validate(user)
    return GetVideo.model_validate(video)


async def delete_video(video_id, user: UserDB, session: AsyncSession) -> GetVideo:
    crud_video = CRUDVideo(VideoDB, session)
    video = await crud_video.delete(video_id)
    if not video:
        raise VideoNotFoundException()
    video.user = UserRead.model_validate(user)
    file_name = video.file
    os.remove(file_name)
    return GetVideo.model_validate(video)


def _generate_file_name(user_id: UUID, file_format: str):
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
    crud_user = CRUDUser(UserDB, session)
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
        raise VideoNotFoundException

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


async def create_subscription(
        user: UUID,
        subscriber: UUID,
        session: AsyncSession,
) -> SubscriberCreate:
    crud_user = CRUDUser(UserDB, session)
    user_for_follow_db = await crud_user.get(user)
    subscriber_db = await crud_user.get(subscriber)
    if not user_for_follow_db:
        raise UserNotFoundException()
    elif user_for_follow_db == subscriber_db:
        raise HTTPException(status_code=403, detail='You can\'t subscribe to yourself')
    followers = await get_user_subscribers(user, session)
    if UserRead.model_validate(subscriber_db) in followers.subscribers:
        raise HTTPException(status_code=400, detail='You have already subscribed')

    subscription = SubscriberCreate(user=user, subscriber=subscriber)
    crud_subscription = CRUDSubscription(SubscriptionDB, session)
    await crud_subscription.create(subscription)
    return subscription


async def delete_subscription(
        user: UUID,
        subscriber: UUID,
        session: AsyncSession,
) -> SubscriberCreate:
    crud_user = CRUDUser(UserDB, session)
    user_for_unfollow_db = await crud_user.get(user)
    subscriber_db = await crud_user.get(subscriber)
    if not user_for_unfollow_db:
        raise UserNotFoundException()
    elif user_for_unfollow_db == subscriber_db:
        raise HTTPException(status_code=403, detail='You can\'t unsubscribe to yourself')

    subscription = SubscriberCreate(user=user, subscriber=subscriber)
    crud_subscription = CRUDSubscription(SubscriptionDB, session)
    subscription = await crud_subscription.delete(subscription)
    if not subscription:
        raise HTTPException(status_code=400, detail='You aren\'t subscribed')
    return SubscriberCreate.model_validate(subscription)


async def get_user_subscribers(
    user: UUID,
    session: AsyncSession = Depends(get_session),
) -> SubscriberList:
    crud_user = CRUDUser(UserDB, session)
    user_db = await crud_user.get(user)
    crud_subscription = CRUDSubscription(SubscriptionDB, session)
    subscribers = await crud_subscription.get_user_subscribers(user)
    follower_list = SubscriberList(user=user_db, subscribers=[])
    for subscriber in subscribers:
        subscriber = await crud_user.get(subscriber.subscriber)
        follower_list.subscribers.append(UserRead.model_validate(subscriber))
    return follower_list


async def get_user_subscriptions(
    user: UUID,
    session: AsyncSession = Depends(get_session),
) -> SubscriptionList:
    crud_user = CRUDUser(UserDB, session)
    user_db = await crud_user.get(user)
    crud_subscription = CRUDSubscription(SubscriptionDB, session)
    subscriptions = await crud_subscription.get_user_subscriptions(user)
    subscription_list = SubscriptionList(user=user_db, subscriptions=[])
    for subscription in subscriptions:
        user = await crud_user.get(subscription.user)
        subscription_list.subscriptions.append(UserRead.model_validate(user))
    return subscription_list


async def delete_user(user_id: UUID, session: AsyncSession) -> UserRead:
    crud_user = CRUDUser(UserDB, session)
    user = await crud_user.delete(user_id)
    return UserRead.model_validate(user)


async def add_or_delete_like(
        video_id: int,
        session: AsyncSession,
        current_user: UserDB,
) -> VideoDB | None:
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
    return video
