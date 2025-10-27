from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    is_manager: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # remove user essentially, if false cant login
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
  
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("managers.id", ondelete="SET NULL"), nullable=True)
    manager = relationship("Manager")
