from typing import cast
from uuid import UUID

from sqlalchemy import delete, select

from backend.crud import CRUDBase
from backend.models import SubscriptionDB
from backend.schemas import SubscriberCreate


class CRUDSubscription(CRUDBase[SubscriptionDB, SubscriberCreate]):
    async def delete(self, subscription: SubscriberCreate) -> SubscriptionDB:
        query = delete(self.model) \
            .where((self.model.user == subscription.user) & (self.model.subscriber == subscription.subscriber)) \
            .returning(self.model)
        subscription = await self.session.execute(query)
        await self.session.commit()
        return subscription.scalar_one_or_none()

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
