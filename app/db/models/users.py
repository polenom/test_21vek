from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.db.models import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    dish_of_the_day: Mapped[str] = mapped_column(String(255), nullable=True)
