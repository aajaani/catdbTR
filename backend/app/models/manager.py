from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
import enum

class StatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class RoleEnum(str, enum.Enum): 
    MANAGER = "MANAGER"
    NOT_MANAGER = "NOT_MANAGER"


class Manager(Base):
    __tablename__ = "managers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(200))
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), nullable=False, default=StatusEnum.ACTIVE)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False, default=RoleEnum.NOT_MANAGER)
