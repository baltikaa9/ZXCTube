import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db import Base
from backend.models import UserDB


class VideoDB(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    file: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    user: Mapped[UUID] = mapped_column(ForeignKey(UserDB.id))
    like_count: Mapped[int] = mapped_column(default=0)
    preview: Mapped[str] = mapped_column(nullable=True)
    like = relationship('VideoLikeDB', cascade='delete')


class VideoLikeDB(Base):
    __tablename__ = 'videos_likes'

    id: Mapped[int] = mapped_column(primary_key=True)
    video: Mapped[int] = mapped_column(ForeignKey(VideoDB.id))
    user: Mapped[UUID] = mapped_column(ForeignKey(UserDB.id))
