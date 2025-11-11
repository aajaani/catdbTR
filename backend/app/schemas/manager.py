from .common import ORMBase
from pydantic import BaseModel
from typing import Literal

Status = Literal["ACTIVE", "INACTIVE"]
Role = Literal["MANAGER", "NOT_MANAGER"]

class ManagerCreate(BaseModel):
    display_name: str
    phone: str | None = None
    email: str | None = None
    status: Status = "ACTIVE"
    role: Role


class ManagerRead(ORMBase):
    id: int
    display_name: str
    phone: str | None = None
    email: str | None = None
    status: Status
    role: Role
