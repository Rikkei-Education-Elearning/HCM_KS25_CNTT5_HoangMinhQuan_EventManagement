from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.db.database import Base
from app.models.user import User

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    users: Mapped[List[User]] = relationship("User", back_populates="role")