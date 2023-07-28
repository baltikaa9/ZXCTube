from uuid import UUID

from pydantic import BaseModel

from schemas import UserRead


class SubscriberCreate(BaseModel):
    user: UUID


class SubscriberList(BaseModel):
    user: UserRead
    subscribers: list[UserRead]


class SubscriptionList(BaseModel):
    user: UserRead
    subscriptions: list[UserRead]
