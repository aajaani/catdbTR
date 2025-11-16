from typing import Sequence
from sqlalchemy import select, update
from app.repositories.base_repository import BaseRepository
from app.models.foster_home import FosterHome

class FosterHomeRepository(BaseRepository):
    def create(self, f: FosterHome) -> FosterHome:
        # SQL: insert new foster home and return it
        self.db.add(f)
        self.db.commit()
        self.db.refresh(f)
        return f
    
    def get(self, home_id: int) -> FosterHome | None:
        stmt = select(FosterHome).where(FosterHome.id == home_id)
        return self.db.execute(stmt).scalars().first()

    def list_all(self) -> Sequence[FosterHome]:
        # SQL: select all foster homes ordered by id
        stmt = select(FosterHome).order_by(FosterHome.id.asc())
        return self.db.execute(stmt).scalars().all()
    
    def update(self, home_id: int, data: dict[str, str]) -> FosterHome | None:
        if not data:
            # nothing to update
            return self.get(home_id)

        stmt = (
            update(FosterHome)
            .where(FosterHome.id == home_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        res = self.db.execute(stmt)
        # if query did not update anything, dont do anything
        if res.rowcount == 0:
            self.db.rollback()
            return None
        self.db.commit()
        return self.get(home_id)
