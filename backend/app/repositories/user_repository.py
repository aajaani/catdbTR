from typing import Sequence
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.user import User
from app.models.account import Account
from app.models.role import Role

class UserRepository(BaseRepository):
    def create(
        self,
        user: User
    ):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).join(User.account).where(Account.username == username)
        return self.db.execute(stmt).scalars().first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
    
    def get_by_role_name(self, role: str | None) -> Sequence[User]:
        stmt = select(User)

        if role is not None:
            stmt = stmt.join(Role).where(Role.name == role)
        return self.db.execute(stmt).scalars().all()

