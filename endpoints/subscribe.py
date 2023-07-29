from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.user_manager import current_active_user
from db import get_session
from models import UserDB
from schemas import SubscriberCreate
from services import create_subscription, delete_subscription

router = APIRouter()


@router.post('/')
async def subscribe(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> SubscriberCreate:
    subscription = await create_subscription(user, current_user.id, session)
    return subscription


@router.delete('/')
async def unsubscribe(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> SubscriberCreate:
    subscription = await delete_subscription(user, current_user.id, session)
    return subscription
