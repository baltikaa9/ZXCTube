from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.api.dependencies import get_session
from backend.models import UserDB
from backend.schemas import SubscriberCreate
from backend.services import SubscriptionService

router = APIRouter(prefix='/subscribe', tags=['Subscribe'])


@router.post('/')
async def subscribe(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user),
        service: SubscriptionService = Depends()
) -> SubscriberCreate:
    subscription = await service.create_subscription(user, current_user.id, session)
    return subscription


@router.delete('/')
async def unsubscribe(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user),
        service: SubscriptionService = Depends()
) -> SubscriberCreate:
    subscription = await service.delete_subscription(user, current_user.id, session)
    return subscription
