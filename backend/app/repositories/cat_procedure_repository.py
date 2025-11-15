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
    
    # get procedure by id for a cat
    def get_by_id(self, cat_id: int, procedure_id: int) -> CatProcedure | None:
        return self.db.query(CatProcedure).filter_by(id=procedure_id, cat_id=cat_id).first()
    
    # update procedure for a cat
    def update(self, procedure_id: int, cat_id: int, data: dict) -> CatProcedure | None:
        proc = self.db.query(CatProcedure).filter_by(id=procedure_id, cat_id=cat_id).first()
        if not proc:
            return None

        for key, value in data.items():
            setattr(proc, key, value)

        self.db.commit()
        self.db.refresh(proc)
        return proc

