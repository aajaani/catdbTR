from .common import ORMBase
# allows nested models (cats can nest ManagerRef and FosterHomeRef, might be pointless)

class ManagerRef(ORMBase):
    id: int
    display_name: str
    phone: str | None = None
    email: str | None = None

class FosterHomeRef(ORMBase):
    id: int
    name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None
