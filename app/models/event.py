from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Mapped, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.user import User
from app.models.role import Role
from app.db.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    owner: Mapped[User] = relationship("User", back_populates="events")


class EventStaff(Base):
    __tablename__ = "event_staff"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    role: Mapped[Role] = relationship("Role", back_populates="event_staff")
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
