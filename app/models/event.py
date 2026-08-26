from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.event_task import EventTask
from app.db.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    staff: Mapped[list["EventStaff"]] = relationship("EventStaff", back_populates="event", cascade="all, delete-orphan")
    owner: Mapped["User"] = relationship("User", back_populates="events")
    tasks: Mapped[list["EventTask"]] = relationship("EventTask", back_populates="event", cascade="all, delete-orphan")


class EventStaff(Base):
    __tablename__ = "event_staff"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"), nullable=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    role: Mapped["Role | None"] = relationship("Role", back_populates="event_staff")
    event: Mapped["Event"] = relationship("Event", back_populates="staff")
    user: Mapped["User"] = relationship("User", back_populates="event_staff")
