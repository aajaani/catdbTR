from .common import ORMBase
# mark's favorite things
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

class ColonyRef(ORMBase):
    id: int
    name: str