from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.role import Role

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    is_manager: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # remove user essentially, if false cant login
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, default=lambda: _get_social_worker_role_id())

    manager_id: Mapped[int | None] = mapped_column(ForeignKey("managers.id", ondelete="SET NULL"), nullable=True)
    manager = relationship("Manager")


def _get_social_worker_role_id():
    from sqlalchemy import select
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        role = db.execute(select(Role).where(Role.name == "SOCIAL_WORKER")).scalars().first()
        return role.id if role else RuntimeError("SOCIAL_WORKER role not found")
    finally:
        db.close()

