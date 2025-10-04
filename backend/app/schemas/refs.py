from .common import ORMBase
# Viited teistele objektidele, nt kassile, varjupaigale, hooldajale

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
