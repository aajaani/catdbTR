from typing import Any
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.schemas.colony import ColonyCreate

from app.models.colony import Colony
from app.models.cat import Cat

from app.repositories.colony_repository import ColonyRepository

from app.utils.audit import log_action


class ColonyService:
    def __init__(self, repo: ColonyRepository):
        self.repo = repo

    def create(self, data: ColonyCreate) -> Colony:
        if not data.name or not data.name.strip():
            raise HTTPException(status_code=422, detail="name is required")

        # name must be unique (case-sensitive)
        name_trim = data.name.strip()
        if self.repo.get_by_name(name_trim):
            raise HTTPException(status_code=409, detail="cat name must be unique")

        if data.cat_ids is not None:
            cats = self.repo.db.execute(select(Cat).where(Cat.id.in_(data.cat_ids))).all( )
        else:
            cats = [ ]

        colony = Colony(
            name=name_trim,
            notes=data.notes,
            cats=cats
        )

        try:
            added_colony = self.repo.create(colony)
        except IntegrityError:
            # topelt-kaitse, kui paralleelselt lisatakse sama nimega
            raise HTTPException(status_code=409, detail="colony name must be unique")

        log_action(self.repo.db, "colony", added_colony.id, "CREATE")
        return added_colony


    def list_all(self) -> list[Colony]:
        return list(self.repo.list_all())
    
    def get_by_id(self, colony_id: int) -> Colony:
        colony = self.repo.get_by_id(colony_id)
        if colony is None:
            raise HTTPException(status_code=404, detail="colony not found")
        return colony
    
    def update(self, colony_id: int, payload: ColonyCreate) -> Colony | None:
        data = payload.model_dump(exclude_unset=True)
        
        data_with_cats: dict[str, Any] = { k: v for ( k, v ) in data if k not in [ "cat_ids" ] }

        if payload.cat_ids is not None:
            cats = self.repo.db.execute(select(Cat).where(Cat.id.in_(payload.cat_ids))).scalars().all()
            data_with_cats[ "cats" ] = list( cats )

        updated_colony = self.repo.update(colony_id, data_with_cats)
        if updated_colony:
            log_action(self.repo.db, "colony", updated_colony.id, "UPDATE") 
        return updated_colony
    
    def delete(self, colony: Colony) -> None:
        self.repo.delete(colony)
        log_action(self.repo.db, "colony", colony.id, "DELETE")