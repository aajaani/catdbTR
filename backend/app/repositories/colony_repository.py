from typing import Sequence
from sqlalchemy import select, update
from app.repositories.base_repository import BaseRepository
from app.models.cat import Cat
from app.models.colony import Colony

class ColonyRepository(BaseRepository):
    def create(self, colony: Colony) -> Colony:
        self.db.add(colony)
        self.db.commit()
        self.db.refresh(colony)
        return colony

    def list_all(self) -> Sequence[Colony]:
        return self.db.execute(select(Colony)).scalars().all()

    def get_by_id(self, colony_id: int) -> Colony | None:
        stmt = select(Colony).where(Colony.id == colony_id)
        return self.db.execute(stmt).scalars().first()
    
    def get_cats_in_colony(self, colony_id: int) -> Sequence[Cat]:
        colony = self.get_by_id(colony_id)

        if colony is None:
            return []
        
        stmt = select(Cat).where(Cat.colony == colony)
        return self.db.execute(stmt).scalars().all()

    # str -> name, notes, int -> id, list[int] -> cat ids
    def update(self, colony_id: int, data: dict[str, str | int | list[int]]) -> Colony | None:
        if not data:
            return self.get_by_id(colony_id)
        
        stmt = (
            update(Colony)
            .where(Colony.id == colony_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        res = self.db.execute(stmt)
        # if query did not update anything, dont do anything
        if res.rowcount == 0:
            self.db.rollback()
            return None
        self.db.commit()
        return self.get_by_id(colony_id)

    def delete(self, colony: Colony) -> None:
        self.db.delete(colony)
        self.db.commit()

    def get_by_name(self, name: str) -> Colony | None:
        stmt = select(Colony).where(Colony.name == name)
        return self.db.execute(stmt).scalars().first()