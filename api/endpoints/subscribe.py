from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user_from_headers
from api.dependencies import get_session
from models import UserDB
from schemas import SubscriberCreate
from services import SubscriptionService

router = APIRouter(prefix='/subscribe', tags=['Subscribe'])


@router.post('/')
async def subscribe(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user_from_headers),
        service: SubscriptionService = Depends()
) -> SubscriberCreate:
    subscription = await service.create_subscription(user, current_user.id, session)
    return subscription


@router.delete('/')
async def unsubscribe(
        user: UUID,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user_from_headers),
        service: SubscriptionService = Depends()
) -> SubscriberCreate:
    subscription = await service.delete_subscription(user, current_user.id, session)
    return subscription
