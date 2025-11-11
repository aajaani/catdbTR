from typing import List
from pydantic import BaseModel


class PermissionRead(BaseModel):
    permission: str

    class ConfigDict:
        from_attributes = True


class RoleRead(BaseModel):
    id: int
    name: str
    permissions: List[PermissionRead]

    class ConfigDict:
        from_attributes = True