from typing import Sequence
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.task import Task

class TaskRepository(BaseRepository):
    def create(self, t: Task) -> Task:
        self.db.add(t)
        self.db.commit()
        self.db.refresh(t)
        return t

    #  list all tasks (most recent first)
    def list_all(self) -> Sequence[Task]:
        stmt = select(Task).order_by(Task.due_date.desc(), Task.id.desc())
        return self.db.execute(stmt).scalars().all()

    #  list all tasks for a cat (most recent first)
    def list_by_cat(self, cat_id: int) -> Sequence[Task]:
        stmt = select(Task).where(Task.cat_id == cat_id).order_by(Task.due_date.desc(), Task.id.desc())
        return self.db.execute(stmt).scalars().all()
