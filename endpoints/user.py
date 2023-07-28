from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import services
from auth.user_manager import fastapi_users, auth_backend, current_active_user
from db.session import get_session
from models import UserDB
from schemas import GetListVideo, UserRead, UserCreate, UserUpdate
from schemas.subscription import SubscriberList, SubscriptionList

router = APIRouter()


@router.get('/me')
async def get_me(
        current_user: UserDB = Depends(current_active_user),
) -> UserRead:
    return UserRead.model_validate(current_user)


@router.get('/{user_id}/videos')
async def get_user_videos(
        user_id: UUID,
        session: AsyncSession = Depends(get_session)
) -> list[GetListVideo]:
    return await services.get_videos_by_user(user_id, session)


@router.get('/me/subscribers')
async def get_my_followers(
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> SubscriberList:
    followers = await services.get_subscribers_by_user(current_user.id, session)
    return followers


@router.get('/me/subscriptions')
async def get_my_followers(
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> SubscriptionList:
    subscriptions = await services.get_user_subscriptions(current_user.id, session)
    return subscriptions


@router.get('/{user_id}/subscribers')
async def get_subscribers(
        user: UUID,
        session: AsyncSession = Depends(get_session),
) -> SubscriberList:
    subscribers = await services.get_subscribers_by_user(user, session)
    return subscribers


@router.get('/{user_id}/subscriptions')
async def get_subscriptions(
        user: UUID,
        session: AsyncSession = Depends(get_session),
) -> SubscriptionList:
    subscriptions = await services.get_user_subscriptions(user, session)
    return subscriptions


router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

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
