import enum
from datetime import date
from sqlalchemy import Integer, String, Enum, ForeignKey, Text, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class SexEnum(str, enum.Enum):
    male = "male"
    female = "female"
    unknown = "unknown"

class StatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    FOSTER = "FOSTER"
    ADOPTED = "ADOPTED"
    ARCHIVED = "ARCHIVED"
    MISSING = "MISSING"
    RESERVED = "RESERVED"

class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # unikaalne nimi, et FE saaks turvaliselt autocomplete teha
    name: Mapped[str] = mapped_column(String(200), index=True, unique=True, nullable=False)

    sex: Mapped[SexEnum | None] = mapped_column(Enum(SexEnum), default=SexEnum.unknown)
    chip_number: Mapped[str | None] = mapped_column(String(30))
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), default=StatusEnum.ACTIVE)

    # links
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("managers.id", ondelete="SET NULL"))
    foster_home_id: Mapped[int | None] = mapped_column(ForeignKey("foster_homes.id", ondelete="SET NULL"))
    colony_id: Mapped[int | None] = mapped_column(ForeignKey("colonies.id", ondelete="SET NULL"))

    # dates
    intake_date: Mapped[date | None] = mapped_column(Date)
    birth_date: Mapped[date | None] = mapped_column(Date)
    foster_end_date: Mapped[date | None] = mapped_column(Date)

    # notes
    notes: Mapped[str | None] = mapped_column(Text)

    # medical (ülejäänud on cat procedures tabelis)
    is_neutered: Mapped[bool | None] = mapped_column(Boolean)

    # media
    primary_photo_object: Mapped[str | None] = mapped_column(String(255))

    # relations
    manager = relationship("Manager")
    foster_home = relationship("FosterHome")
    colony = relationship("Colony", back_populates="cats")
    procedures = relationship("CatProcedure", back_populates="cat", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="cat", cascade="all, delete-orphan")
