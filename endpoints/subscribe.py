from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.user_manager import current_active_user
from db.session import get_session
from models import UserDB, SubscriptionDB
from schemas import UserRead
from schemas.subscription import SubscriberCreate, SubscriberList, SubscriptionList
from services import get_subscribers_by_user, get_user_subscriptions

router = APIRouter()


@router.post('/')
async def subscribe(
        user: SubscriberCreate,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> SubscriberCreate:
    subscription_relationship = SubscriptionDB(
        user=user.user,
        subscriber=current_user.id,
    )
    user_for_follow = await session.get(UserDB, user.user)
    if not user_for_follow:
        raise HTTPException(status_code=404, detail='User not found')
    elif user_for_follow.id == current_user.id:
        raise HTTPException(status_code=403, detail='You can\'t subscribe to yourself')
    followers = await get_subscribers_by_user(user.user, session)
    if UserRead.model_validate(current_user) in followers.subscribers:
        raise HTTPException(status_code=400, detail='You have already subscribed')
    session.add(subscription_relationship)
    await session.commit()
    return user


@router.delete('/')
async def unsubscribe(
        user: SubscriberCreate,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> SubscriberCreate:
    return user

# TODO: unfollow, список на кого подписан
