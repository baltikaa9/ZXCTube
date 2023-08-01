from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import current_active_user
from dependencies import get_session
from models import UserDB
from schemas import SubscriberCreate
from services import SubscriptionService

router = APIRouter()


@router.post('/')
async def subscribe(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
        service: SubscriptionService = Depends()
) -> SubscriberCreate:
    subscription = await service.create_subscription(user, current_user.id, session)
    return subscription


@router.delete('/')
async def unsubscribe(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
        service: SubscriptionService = Depends()
) -> SubscriberCreate:
    subscription = await service.delete_subscription(user, current_user.id, session)
    return subscription
