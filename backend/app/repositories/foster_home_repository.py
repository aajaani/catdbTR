from typing import Sequence
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.foster_home import FosterHome

class FosterHomeRepository(BaseRepository):
    def create(self, f: FosterHome) -> FosterHome:
        # SQL: insert new foster home and return it
        self.db.add(f)
        self.db.commit()
        self.db.refresh(f)
        return f

    def list_all(self) -> Sequence[FosterHome]:
        # SQL: select all foster homes ordered by id
        stmt = select(FosterHome).order_by(FosterHome.id.asc())
        return self.db.execute(stmt).scalars().all()
