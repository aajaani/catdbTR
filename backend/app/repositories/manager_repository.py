from typing import Sequence
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.manager import Manager

class ManagerRepository(BaseRepository):
    def create(self, m: Manager) -> Manager:
        # SQL: INSERT INTO managers (display_name, phone, email) VALUES (...) RETURNING *
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        return m

    def list_all(self) -> Sequence[Manager]:
        # SQL: SELECT * FROM managers ORDER BY id ASC
        stmt = select(Manager).order_by(Manager.id.asc())
        return self.db.execute(stmt).scalars().all()
