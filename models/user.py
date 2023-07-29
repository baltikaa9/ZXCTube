from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class UserDB(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(nullable=False)
    videos: Mapped[list['VideoDB']] = relationship()
