from app.models.role import Role

from app.schemas.role import RoleRead

from app.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    def list_roles(self) -> list[RoleRead]:
        roles: list[Role] = list(self.role_repo.get_all())
        return [ RoleRead(
            id=role.id,
            name=role.name,
            permissions=[permission.permission for permission in role.role_permissions]
        ) for role in roles ]
