from .common import ORMBase
from pydantic import BaseModel

class ManagerCreate(BaseModel):
    display_name: str
    phone: str | None = None
    email: str | None = None

class ManagerRead(ORMBase):
    id: int
    display_name: str
    phone: str | None = None
    email: str | None = None
