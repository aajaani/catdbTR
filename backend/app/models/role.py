from enum import Enum
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey


# NB: not a model
class Permissions(str, Enum):
    # cat create read update delete
    CAT_ADD = "cat:create"  # c
    CAT_VIEW = "cat:read"  # r
    CAT_EDIT = "cat:update"  # u
    CAT_REMOVE = "cat:delete"  # d

    COLONY_ADD = "colony:add"
    COLONY_VIEW = "colony:view"
    COLONY_EDIT = "colony:edit"
    COLONY_REMOVE = "colony:remove"

    USER_ADD = "user:create"
    USER_VIEW = "user:read"
    USER_EDIT = "user:update"
    USER_REMOVE = "user:delete"

    FOSTER_ADD = "foster:create"
    FOSTER_VIEW = "foster:read"
    FOSTER_EDIT = "foster:update"
    FOSTER_REMOVE = "foster:delete"

    PROCEDURE_ADD = "procedures:create"
    PROCEDURE_VIEW = "procedures:read"
    PROCEDURE_EDIT = "procedures:update"
    PROCEDURE_REMOVE = "procedures:delete"

    TASK_ADD = "task:create"
    TASK_VIEW = "task:read"
    TASK_EDIT = "task:update"
    TASK_REMOVE = "task:delete"


class RolePermission(Base):
    __tablename__ = "role_permissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))
    permission: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped["Role"] = relationship("Role", back_populates="role_permissions")


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    role_permissions: Mapped[list["RolePermission"]] = relationship("RolePermission", back_populates="role")

    # used in UserRead converting, could have "role_permissions" instead
    # of "permissions" in UserRead
    @property
    def permissions(self) -> list[str]:
        return [ rp.permission for rp in self.role_permissions]

# created/updated in run
# I kind of see an issue with this approach
# if we want to change permissions (rare, client didn't want aswell)
# we have to edit this file and redeploy to update the db
class _RolePermissionConfig:
    class Roles(str, Enum):
        ADMIN = "ADMIN"
        MANAGER = "MANAGER"
        SOCIAL_WORKER = "SOCIAL_WORKER"

    ADMIN = {
        Permissions.CAT_ADD,
        Permissions.CAT_VIEW,
        Permissions.CAT_EDIT,
        Permissions.CAT_REMOVE,

        Permissions.COLONY_ADD,
        Permissions.COLONY_VIEW,
        Permissions.COLONY_EDIT,
        Permissions.COLONY_REMOVE,

        Permissions.USER_ADD,
        Permissions.USER_VIEW,
        Permissions.USER_EDIT,
        Permissions.USER_REMOVE,

        Permissions.FOSTER_ADD,
        Permissions.FOSTER_VIEW,
        Permissions.FOSTER_EDIT,
        Permissions.FOSTER_REMOVE,

        Permissions.PROCEDURE_ADD,
        Permissions.PROCEDURE_VIEW,
        Permissions.PROCEDURE_EDIT,
        Permissions.PROCEDURE_REMOVE,

        Permissions.TASK_ADD,
        Permissions.TASK_VIEW,
        Permissions.TASK_EDIT,
        Permissions.TASK_REMOVE,
    }

    MANAGER = {
        Permissions.CAT_ADD,
        Permissions.CAT_VIEW,
        Permissions.CAT_EDIT,
        Permissions.CAT_REMOVE,

        Permissions.COLONY_ADD,
        Permissions.COLONY_VIEW,
        Permissions.COLONY_EDIT,
        Permissions.COLONY_REMOVE,

        Permissions.USER_ADD,
        Permissions.USER_VIEW,
        Permissions.USER_EDIT,
        Permissions.USER_REMOVE,

        Permissions.FOSTER_ADD,
        Permissions.FOSTER_VIEW,
        Permissions.FOSTER_EDIT,
        Permissions.FOSTER_REMOVE,

        Permissions.PROCEDURE_ADD,
        Permissions.PROCEDURE_VIEW,
        Permissions.PROCEDURE_EDIT,
        Permissions.PROCEDURE_REMOVE,

        Permissions.TASK_ADD,
        Permissions.TASK_VIEW,
        Permissions.TASK_EDIT,
        Permissions.TASK_REMOVE,
    }

    # lowk rename this
    SOCIAL_WORKER = {
        Permissions.CAT_VIEW,
        Permissions.COLONY_VIEW,
        Permissions.USER_VIEW,
        Permissions.FOSTER_VIEW,
        Permissions.PROCEDURE_VIEW,
        Permissions.TASK_VIEW,
    }

    def get_role_permissions(self, role_name: str) -> set[Permissions] | None:
        return getattr(self, role_name, None)

# singleton for inner class (i like c syntax)
RolePermissionConfig = _RolePermissionConfig