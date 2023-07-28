from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from models import UserDB


class FollowerDB(Base):
    __tablename__ = 'followers'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[UUID] = mapped_column(ForeignKey(UserDB.id))
    subscriber: Mapped[UUID] = mapped_column(ForeignKey(UserDB.id))
