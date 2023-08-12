from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import CRUDUser, CRUDSubscription
from exceptions import UserNotFoundException
from models import UserDB, SubscriptionDB
from schemas import SubscriberCreate, UserRead, SubscriberList, SubscriptionList


class SubscriptionService:
    async def create_subscription(
            self,
            user: UUID,
            subscriber: UUID,
            session: AsyncSession,
    ) -> SubscriberCreate:
        crud_user = CRUDUser(UserDB, session)
        user_for_follow_db = await crud_user.get(user)
        subscriber_db = await crud_user.get(subscriber)
        if not user_for_follow_db:
            raise UserNotFoundException()
        elif user_for_follow_db == subscriber_db:
            raise HTTPException(status_code=403, detail='You can\'t subscribe to yourself')
        followers = await self.get_user_subscribers(user, session)
        if UserRead.model_validate(subscriber_db) in followers.subscribers:
            raise HTTPException(status_code=400, detail='You have already subscribed')

        subscription = SubscriberCreate(user=user, subscriber=subscriber)
        crud_subscription = CRUDSubscription(SubscriptionDB, session)
        await crud_subscription.create(subscription)
        return subscription

    @staticmethod
    async def delete_subscription(
            user: UUID,
            subscriber: UUID,
            session: AsyncSession,
    ) -> SubscriberCreate:
        crud_user = CRUDUser(UserDB, session)
        user_for_unfollow_db = await crud_user.get(user)
        subscriber_db = await crud_user.get(subscriber)
        if not user_for_unfollow_db:
            raise UserNotFoundException()
        elif user_for_unfollow_db == subscriber_db:
            raise HTTPException(status_code=403, detail='You can\'t unsubscribe to yourself')

        subscription = SubscriberCreate(user=user, subscriber=subscriber)
        crud_subscription = CRUDSubscription(SubscriptionDB, session)
        subscription = await crud_subscription.delete(subscription)
        if not subscription:
            raise HTTPException(status_code=400, detail='You aren\'t subscribed')
        return SubscriberCreate.model_validate(subscription)

    @staticmethod
    async def get_user_subscribers(
        user: UUID,
        session: AsyncSession,
    ) -> SubscriberList:
        crud_user = CRUDUser(UserDB, session)
        user_db = await crud_user.get(user)
        crud_subscription = CRUDSubscription(SubscriptionDB, session)
        subscribers = await crud_subscription.get_user_subscribers(user)
        follower_list = SubscriberList(user=user_db, subscribers=[])
        for subscriber in subscribers:
            subscriber = await crud_user.get(subscriber.subscriber)
            follower_list.subscribers.append(UserRead.model_validate(subscriber))
        return follower_list

    @staticmethod
    async def get_user_subscriptions(
        user: UUID,
        session: AsyncSession,
    ) -> SubscriptionList:
        crud_user = CRUDUser(UserDB, session)
        user_db = await crud_user.get(user)
        crud_subscription = CRUDSubscription(SubscriptionDB, session)
        subscriptions = await crud_subscription.get_user_subscriptions(user)
        subscription_list = SubscriptionList(user=user_db, subscriptions=[])
        for subscription in subscriptions:
            user = await crud_user.get(subscription.user)
            subscription_list.subscriptions.append(UserRead.model_validate(user))
        return subscription_list
