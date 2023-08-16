from uuid import uuid4, UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db import Base


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    picture: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)

    video = relationship('VideoDB', cascade='delete')
    like = relationship('VideoLikeDB', cascade='delete')
    subscription = relationship('SubscriptionDB', cascade='delete', foreign_keys='SubscriptionDB.user')
    subscriber = relationship('SubscriptionDB', cascade='delete', foreign_keys='SubscriptionDB.subscriber')
    token = relationship('RefreshTokenDB', cascade='delete')
