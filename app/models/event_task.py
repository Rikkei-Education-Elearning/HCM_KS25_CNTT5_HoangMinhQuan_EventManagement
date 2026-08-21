from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.user import User
from app.db.database import Base


class EventTask(Base):
    __tablename__ = "event_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    attachments: Mapped[str] = mapped_column(Text, nullable=True)
    assignee: Mapped[User] = relationship("User", back_populates="event_tasks")
    status: Mapped[str] = mapped_column(String(255), default="pending")
    priority: Mapped[str] = mapped_column(String(255), default="medium")
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
