from app.db.base import Base

from sqlalchemy import Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # link to login_user
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), unique=True, nullable=False)

    email: Mapped[str] = mapped_column(String(100), unique= True, nullable= False)

    # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-one
    account = relationship("Account", back_populates="user", uselist=False)

    # link to user role
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)    
    role = relationship("Role")

    display_name = mapped_column(String(100), nullable=False)

    # remove user essentially, if false cant login
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    phone = mapped_column(String(16), nullable=True, default=None)
