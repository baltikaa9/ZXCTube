import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from models.user import UserDB


class VideoDB(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    file: Mapped[str] = mapped_column(nullable=False)
    create_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    user: Mapped[int] = mapped_column(ForeignKey(UserDB.id, ondelete='restrict'))
