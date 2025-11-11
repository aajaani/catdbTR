from typing import List
from pydantic import BaseModel

class RoleRead(BaseModel):
    id: int
    name: str

    # from @proprerty on Role model
    permissions: List[str]

    class ConfigDict:
        from_attributes = True