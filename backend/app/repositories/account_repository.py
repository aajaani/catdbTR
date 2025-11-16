from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.user import User
from app.models.account import Account

class AccountRepository(BaseRepository):
    def create(
        self,
        account: Account,
    ):
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).join(User.account).where(Account.username == username)
        return self.db.execute(stmt).scalars().first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
