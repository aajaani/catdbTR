from datetime import date

from app.models.task import Task, TaskTypeEnum

from app.repositories.task_repository import TaskRepository
from app.repositories.cat_repository import CatRepository

from app.utils.audit import log_action
from fastapi import HTTPException

class TaskService:
    def __init__(self, repo: TaskRepository, cat_repo: CatRepository):
        self.repo = repo
        self.cat_repo = cat_repo

    # add new task for cat
    def add(self, cat_id: int, type_: str, due_date: date, notes: str | None) -> Task:
        if self.cat_repo.get_with_related(cat_id) is None:
            raise HTTPException(status_code=404, detail="cat not found")

        t = Task(cat_id=cat_id, type=TaskTypeEnum(type_), due_date=due_date, notes=notes)
        t = self.repo.create(t)
        log_action(self.repo.db, "task", t.id, "CREATE")
        return t

    def list_all(self) -> list[Task]:
        return list(self.repo.list_all())

    def list_by_cat(self, cat_id: int) -> list[Task]:
        return list(self.repo.list_by_cat(cat_id))
