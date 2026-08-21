from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.db.database import Base
from datetime import datetime
from app.models.role import Role

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[Role] = relationship("Role", back_populates="users")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)