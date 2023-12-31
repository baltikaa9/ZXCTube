from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base
from backend.models import UserDB


class SubscriptionDB(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[UUID] = mapped_column(ForeignKey(UserDB.id))
    subscriber: Mapped[UUID] = mapped_column(ForeignKey(UserDB.id))
