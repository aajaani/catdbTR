from datetime import date
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.cat import Cat
from app.repositories.task_repository import TaskRepository
from app.repositories.cat_repository import CatRepository
from app.services.task_service import TaskService
from fastapi import HTTPException


@pytest.fixture()
def task_service():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = Session()

    svc = TaskService(TaskRepository(db), CatRepository(db))
    try:
        yield svc, db
    finally:
        db.close()
        engine.dispose()


def test_add_task_for_missing_cat_404(task_service):
    svc, db = task_service

    with pytest.raises(HTTPException) as exc:
        svc.add(cat_id=999, type_="VET_VISIT", due_date=date.today(), notes=None)

    assert exc.value.status_code == 404


def test_add_task_for_existing_cat(task_service):
    svc, db = task_service

    cat = Cat(name="Muru")
    db.add(cat)
    db.commit()
    db.refresh(cat)

    task = svc.add(cat_id=cat.id, type_="VET_VISIT", due_date=date(2024, 10, 1), notes="checkup")

    assert task.id is not None
    assert task.cat_id == cat.id
    assert task.type.name == "VET_VISIT"
