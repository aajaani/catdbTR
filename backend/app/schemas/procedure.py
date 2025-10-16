from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel
from .common import ORMBase

ProcedureType = Literal["DEWORMER", "SPOT_ON", "VACCINE"]

class ProcedureCreate(BaseModel):
    type: ProcedureType
    is_repeat: bool = False
    at_date: date
    notes: str | None = None
    payment: int | None = None

class ProcedureRead(ORMBase):
    id: int
    cat_id: int
    type: ProcedureType
    is_repeat: bool
    at_date: date
    notes: str | None = None
    file_object: str | None = None
    payment: int | None = None
