from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    def create(self, u: User) -> User:
        self.db.add(u)
        self.db.commit()
        self.db.refresh(u)
        return u

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.execute(stmt).scalars().first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
