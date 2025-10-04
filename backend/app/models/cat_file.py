from datetime import datetime
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class CatFile(Base):
    __tablename__ = "cat_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cat_id: Mapped[int] = mapped_column(ForeignKey("cats.id", ondelete="CASCADE"), nullable=False)
    object_name: Mapped[str] = mapped_column(String(255), nullable=False) # MinIO key
    content_type: Mapped[str | None] = mapped_column(String(100))
    label: Mapped[str | None] = mapped_column(String(200))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cat = relationship("Cat")
