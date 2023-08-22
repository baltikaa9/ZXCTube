from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_session, get_current_user
from backend.exceptions import UserNotFoundException
from backend.models import UserDB
from backend.schemas import GetVideo, UserRead
from backend.schemas import SubscriberList, SubscriptionList
from backend.services import UserService, VideoService, SubscriptionService

router = APIRouter(prefix='/user', tags=['User'])


@router.get('/me')
async def get_me(
        current_user: UserDB = Depends(get_current_user),
) -> UserRead:
    return UserRead.model_validate(current_user)


@router.get('/me/videos')
async def get_my_videos(
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user),
        service: VideoService = Depends()
) -> list[GetVideo]:
    return await service.get_videos_by_user(current_user.id, session)


@router.get('/{user_id}/videos')
@cache(expire=30)
async def get_user_videos(
        user_id: UUID,
        session: AsyncSession = Depends(get_session),
        service: VideoService = Depends()
) -> list[GetVideo]:
    return await service.get_videos_by_user(user_id, session)


@router.get('/me/subscribers')
async def get_my_subscribers(
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user),
        service: SubscriptionService = Depends()
) -> SubscriberList:
    followers = await service.get_user_subscribers(current_user.id, session)
    return followers


@router.get('/me/subscriptions')
async def get_my_subscriptions(
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user),
        service: SubscriptionService = Depends()
) -> SubscriptionList:
    subscriptions = await service.get_user_subscriptions(current_user.id, session)
    return subscriptions


@router.get('/{user_id}/subscribers')
@cache(expire=30)
async def get_subscribers(
        user_id: UUID,
        session: AsyncSession = Depends(get_session),
        service: SubscriptionService = Depends()
) -> SubscriberList:
    subscribers = await service.get_user_subscribers(user_id, session)
    return subscribers


@router.get('/{user_id}/subscriptions')
@cache(expire=30)
async def get_subscriptions(
        user_id: UUID,
        session: AsyncSession = Depends(get_session),
        service: SubscriptionService = Depends()
) -> SubscriptionList:
    subscriptions = await service.get_user_subscriptions(user_id, session)
    return subscriptions


@router.delete('/{user_id}', dependencies=[Depends(get_current_user)])
async def delete_user(
        user_id: UUID,
        session: AsyncSession = Depends(get_session),
        service: UserService = Depends()
) -> UserRead:
    user = await service.delete_user(user_id, session)
    if not user:
        raise UserNotFoundException()
    return user
