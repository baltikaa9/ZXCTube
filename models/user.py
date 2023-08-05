from uuid import uuid4, UUID

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


# class UserDB(SQLAlchemyBaseUserTableUUID, Base):
#     __tablename__ = 'users'
#
#     username: Mapped[str] = mapped_column(nullable=False)
#     videos: Mapped[list['VideoDB']] = relationship()


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(GUID, primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    # phone: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    picture: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
