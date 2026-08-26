from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")
    event_staff: Mapped[list["EventStaff"]] = relationship(
        "EventStaff", back_populates="role"
    )
