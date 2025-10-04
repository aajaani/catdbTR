from typing import Sequence
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.foster_home import FosterHome

class FosterHomeRepository(BaseRepository):
    def create(self, f: FosterHome) -> FosterHome:
        # SQL: INSERT INTO foster_homes (name, phone, email, address, comments) VALUES (...) RETURNING *
        self.db.add(f)
        self.db.commit()
        self.db.refresh(f)
        return f

    def list_all(self) -> Sequence[FosterHome]:
        # SQL: SELECT * FROM foster_homes ORDER BY id ASC
        stmt = select(FosterHome).order_by(FosterHome.id.asc())
        return self.db.execute(stmt).scalars().all()
