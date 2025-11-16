from .common import ORMBase
from pydantic import BaseModel

class FosterHomeCreate(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    comments: str | None = None

class FosterHomeRead(ORMBase):
    id: int
    name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    comments: str | None = None

class FosterHomeUpdate(ORMBase):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    comments: str | None = None