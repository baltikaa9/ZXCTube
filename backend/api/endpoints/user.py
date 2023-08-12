from uuid import UUID

from fastapi import APIRouter, Depends
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
async def get_subscribers(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        service: SubscriptionService = Depends()
) -> SubscriberList:
    subscribers = await service.get_user_subscribers(user, session)
    return subscribers


@router.get('/{user_id}/subscriptions')
async def get_subscriptions(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        service: SubscriptionService = Depends()
) -> SubscriptionList:
    subscriptions = await service.get_user_subscriptions(user, session)
    return subscriptions


# router.include_router(
#     _fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
# )
#
# router.include_router(
#     _fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )


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

# router.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
#
# router.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
#
# router.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )
