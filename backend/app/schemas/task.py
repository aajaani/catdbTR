from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel
from .common import ORMBase

TaskType = Literal[
    "VET_VISIT",
    "MEDICATION",
    "PERSONAL"
]

class TaskCreate(BaseModel):
    cat_id: int
    type: TaskType
    due_date: date
    notes: str | None = None

class TaskRead(ORMBase):
    id: int
    cat_id: int
    type: TaskType
    due_date: date
    notes: str | None = None
