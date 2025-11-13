from typing import Sequence
from sqlalchemy import select, update
from app.repositories.base_repository import BaseRepository
from app.models.user import User
from app.models.account import Account
from app.models.role import Role
from app.schemas.user import UserUpdate

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
        else:
            stmt = stmt.join(Role)
        
        return self.db.execute(stmt).scalars().all()
    
    def update(self, user_id: int, data: dict[str, int | str | bool]) -> User | None:
        if not data:
            return self.get_by_id(user_id)
        
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        
        res = self.db.execute(stmt)

        if res.rowcount == 0:
            self.db.rollback()
            return None
        
        self.db.commit()
        return self.get_by_id(user_id)
    
    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()

