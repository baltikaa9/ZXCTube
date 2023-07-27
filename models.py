import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    videos: Mapped[list['VideoDB']] = relationship()


class VideoDB(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    file: Mapped[str] = mapped_column(nullable=False)
    create_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    user: Mapped[int] = mapped_column(ForeignKey(UserDB.id, ondelete='restrict'))
