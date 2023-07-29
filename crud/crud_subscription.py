from typing import Type, cast
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud import CRUDBase
from models import SubscriptionDB
from schemas import SubscriberCreate


class CRUDSubscription(CRUDBase[SubscriptionDB, SubscriberCreate]):
    async def delete(self, subscription: SubscriberCreate) -> SubscriptionDB:
        query = delete(self.model) \
            .where((self.model.user == subscription.user) & (self.model.subscriber == subscription.subscriber)) \
            .returning(SubscriptionDB)
        subscription = await self.session.execute(query)
        await self.session.commit()
        subscription = subscription.scalar_one_or_none()
        return subscription

    async def get_user_subscribers(self, user: UUID) -> list[SubscriptionDB]:
        query = select(self.model).where(self.model.user == user)
        subscribers = await self.session.execute(query)
        subscribers = subscribers.scalars().all()
        subscribers = cast(list[SubscriptionDB], subscribers)
        return subscribers

    async def get_user_subscriptions(self, user: UUID) -> list[SubscriptionDB]:
        query = select(self.model).where(self.model.subscriber == user)
        subscribers = await self.session.execute(query)
        subscribers = subscribers.scalars().all()
        subscribers = cast(list[SubscriptionDB], subscribers)
        return subscribers
