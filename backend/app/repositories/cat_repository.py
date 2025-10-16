from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from app.repositories.base_repository import BaseRepository
from app.models.cat import Cat

class CatRepository(BaseRepository):
    def create(self, cat: Cat) -> Cat:
        # SQL: insert new cat and return it
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def get_with_related(self, cat_id: int) -> Cat | None:
        # SQL: select one cat by id (with manager and foster_home)
        stmt = (
            select(Cat)
            .options(
                joinedload(Cat.manager),
                joinedload(Cat.foster_home),
            )
            .where(Cat.id == cat_id)
        )
        return self.db.execute(stmt).scalars().first()

    def list_all_with_related(self) -> Sequence[Cat]:
        # SQL: select all cats (with manager and foster_home)
        stmt = (
            select(Cat)
            .options(
                joinedload(Cat.manager),
                joinedload(Cat.foster_home),
            )
        )
        return self.db.execute(stmt).scalars().all()

    def update(self, cat_id: int, data: dict) -> Cat | None:
        # SQL: update cat by id with partial data and return updated cat (with related)
        # use data dict to set only the fields that are present, so we dont have to load the whole ORM object first
    
        if not data:
            # nothing to update
            return self.get_with_related(cat_id)

        stmt = (
            update(Cat)
            .where(Cat.id == cat_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        res = self.db.execute(stmt)
        # if query did not update anything, dont do anything
        if res.rowcount == 0:
            self.db.rollback()
            return None
        self.db.commit()
        return self.get_with_related(cat_id)

    def delete(self, cat: Cat) -> None:
        self.db.delete(cat)
        self.db.commit()

    # is the name already taken by another cat?
    def get_by_name(self, name: str) -> Cat | None:
        stmt = select(Cat).where(Cat.name == name)
        return self.db.execute(stmt).scalars().first()