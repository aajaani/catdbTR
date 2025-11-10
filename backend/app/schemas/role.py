from pydantic import BaseModel


class PermissionRead(BaseModel):
    permission_name: str


class RoleRead(BaseModel):
    id: int
    name: str
    permissions: list[PermissionRead]