import enum
from datetime import date, datetime
from sqlalchemy import Integer, String, Enum, ForeignKey, Text, Date, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class ProcedureTypeEnum(str, enum.Enum):
    DEWORMER = "DEWORMER" # ussirohi
    SPOT_ON = "SPOT_ON" # turjatilk
    VACCINE = "VACCINE" # vaktsiin

class CatProcedure(Base):
    __tablename__ = "cat_procedures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cat_id: Mapped[int] = mapped_column(ForeignKey("cats.id", ondelete="CASCADE"), nullable=False)

    # procedure type (3 options)
    type: Mapped[ProcedureTypeEnum] = mapped_column(Enum(ProcedureTypeEnum), nullable=False)
    # is it booster/repeat (boolean)
    is_repeat: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    at_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    file_object: Mapped[str | None] = mapped_column(String(255)) # optional file (MinIO key)
    payment: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cat = relationship("Cat", back_populates="procedures")
