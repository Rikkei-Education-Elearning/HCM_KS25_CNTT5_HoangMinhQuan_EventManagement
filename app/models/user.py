from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    role: Mapped["Role | None"] = relationship("Role", back_populates="users")
    events: Mapped[list["Event"]] = relationship("Event", back_populates="owner")
    event_tasks: Mapped[list["EventTask"]] = relationship(
        "EventTask", back_populates="assignee"
    )
    event_staff: Mapped[list["EventStaff"]] = relationship(
        "EventStaff", back_populates="user"
    )
