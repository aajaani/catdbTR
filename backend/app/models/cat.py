import enum
from datetime import date
from sqlalchemy import Integer, String, Enum, ForeignKey, Text, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class SexEnum(str, enum.Enum):
    isane = "isane"
    emane = "emane"
    unknown = "unknown"

class StatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    FOSTER = "FOSTER"
    ADOPTED = "ADOPTED"
    ARCHIVED = "ARCHIVED"
    KADUNUD = "KADUNUD"           # missing
    BRONEERITUD = "BRONEERITUD"   # reserved

class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)

    sex: Mapped[SexEnum | None] = mapped_column(Enum(SexEnum), default=SexEnum.unknown)
    chip_number: Mapped[str | None] = mapped_column(String(30))

    # status incl. BRONEERITUD / KADUNUD
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), default=StatusEnum.ACTIVE)

    # links (nullable)
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("managers.id", ondelete="SET NULL"))
    foster_home_id: Mapped[int | None] = mapped_column(ForeignKey("foster_homes.id", ondelete="SET NULL"))
    colony_id: Mapped[int | None] = mapped_column(ForeignKey("colonies.id", ondelete="SET NULL"))

    # dates
    kk_alates: Mapped[date | None] = mapped_column(Date)       # "KK alates"
    birth_date: Mapped[date | None] = mapped_column(Date)      # age via datepicker
    foster_end: Mapped[date | None] = mapped_column(Date)      # "Hoiu lõpp"

    # text/notes
    location_text: Mapped[str | None] = mapped_column(String(200))  # free-text if needed
    notes: Mapped[str | None] = mapped_column(Text)                 # "Märkmed"

    # medical (Estonian names like in sheet)
    ussitableti_nimi: Mapped[str | None] = mapped_column(String(200))
    ussitablett: Mapped[date | None] = mapped_column(Date)
    ussit_kordus: Mapped[date | None] = mapped_column(Date)

    turjatilga_nimi: Mapped[str | None] = mapped_column(String(200))
    turjatilk: Mapped[date | None] = mapped_column(Date)
    turj_kordus: Mapped[date | None] = mapped_column(Date)

    i_vaktsiin: Mapped[date | None] = mapped_column(Date)
    kordusvax: Mapped[date | None] = mapped_column(Date)

    ster_kastr: Mapped[bool | None] = mapped_column(Boolean)

    # media
    primary_photo_object: Mapped[str | None] = mapped_column(String(255))  # MinIO object key

    # relations
    manager = relationship("Manager")
    foster_home = relationship("FosterHome")
    colony = relationship("Colony", back_populates="cats")
