from typing import Sequence
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.cat_procedure import CatProcedure

class CatProcedureRepository(BaseRepository):
    #  add new procedure for cat
    def create(self, p: CatProcedure) -> CatProcedure:
        self.db.add(p)
        self.db.commit()
        self.db.refresh(p)
        return p

    #  get all procedures for a cat (most recent first)
    def list_by_cat(self, cat_id: int) -> Sequence[CatProcedure]:
        stmt = select(CatProcedure).where(CatProcedure.cat_id == cat_id).order_by(CatProcedure.at_date.desc())
        return self.db.execute(stmt).scalars().all()
