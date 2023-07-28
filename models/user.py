from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    videos: Mapped[list['VideoDB']] = relationship()
