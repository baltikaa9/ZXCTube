from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.user_manager import current_active_user
from db.session import get_session
from models import UserDB, FollowerDB
from schemas import UserRead
from schemas.follower import FollowerCreate, FollowerList
from services import get_followers_by_user

router = APIRouter()


@router.post('/')
async def follow(
        user: FollowerCreate,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> FollowerCreate:
    follower_relationship = FollowerDB(
        user=user.user,
        subscriber=current_user.id,
    )
    user_for_follow = await session.get(UserDB, user.user)
    if not user_for_follow:
        raise HTTPException(status_code=404, detail='User not found')
    elif user_for_follow.id == current_user.id:
        raise HTTPException(status_code=403, detail='You can\'t subscribe to yourself')
    followers = await get_followers_by_user(user.user, session)
    if UserRead.model_validate(current_user) in followers.followers:
        raise HTTPException(status_code=400, detail='You have already subscribed')
    session.add(follower_relationship)
    await session.commit()
    return user


@router.get('/')
async def get_followers(
    user: UUID,
    session: AsyncSession = Depends(get_session),
) -> FollowerList:
    followers = await get_followers_by_user(user, session)
    return followers


@router.delete('/')
async def unfollow(
        user: FollowerCreate,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> FollowerCreate:
    return user

# TODO: unfollow, список на кого подписан
