import enum
from datetime import date, datetime, timezone
from sqlalchemy import Integer, String, Enum, ForeignKey, Text, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class TaskTypeEnum(str, enum.Enum):
    VET_VISIT = "VET_VISIT"  
    MEDICATION = "MEDICATION"      
    PERSONAL = "PERSONAL" 

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cat_id: Mapped[int] = mapped_column(ForeignKey("cats.id", ondelete="CASCADE"), nullable=False)

    type: Mapped[TaskTypeEnum] = mapped_column(Enum(TaskTypeEnum), nullable=False)

    due_date: Mapped[date] = mapped_column(Date, nullable=False)

    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    cat = relationship("Cat", back_populates="tasks")
