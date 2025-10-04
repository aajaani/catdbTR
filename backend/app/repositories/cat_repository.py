from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.repositories.base_repository import BaseRepository
from app.models.cat import Cat

class CatRepository(BaseRepository):
    def create(self, cat: Cat) -> Cat:
        # SQL: INSERT INTO cats (...) VALUES (...) RETURNING *
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def get_with_related(self, cat_id: int) -> Cat | None:
        # SQL:
        # SELECT c.*, m.*, f.*
        # FROM cats c
        # LEFT JOIN managers m ON m.id = c.manager_id
        # LEFT JOIN foster_homes f ON f.id = c.foster_home_id
        # WHERE c.id = :cat_id
        stmt = (
            select(Cat)
            .options(
                joinedload(Cat.manager),      # LEFT OUTER JOIN managers
                joinedload(Cat.foster_home),  # LEFT OUTER JOIN foster_homes
            )
            .where(Cat.id == cat_id)
        )
        return self.db.execute(stmt).scalars().first()

    def list_all_with_related(self) -> Sequence[Cat]:
        # SQL:
        # SELECT c.*, m.*, f.*
        # FROM cats c
        # LEFT JOIN managers m ON m.id = c.manager_id
        # LEFT JOIN foster_homes f ON f.id = c.foster_home_id
        stmt = (
            select(Cat)
            .options(
                joinedload(Cat.manager),      # LEFT OUTER JOIN managers
                joinedload(Cat.foster_home),  # LEFT OUTER JOIN foster_homes
            )
        )
        return self.db.execute(stmt).scalars().all()
