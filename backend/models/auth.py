from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base
from backend.models import UserDB


class RefreshTokenDB(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(UserDB.id), nullable=False)
    token: Mapped[UUID] = mapped_column(unique=True, nullable=False)
