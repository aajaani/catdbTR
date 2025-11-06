from rich import print
from sqlalchemy import select
from passlib.context import CryptContext
from fastapi import HTTPException

from app.models.role import Role, RolePermissionConfig, RolePermission
from app.models.user import User
from app.models.manager import Manager
from app.repositories.manager_repository import ManagerRepository
from app.repositories.user_repository import UserRepository
from app.utils.audit import log_action
from passlib.context import CryptContext

_pwd_ctx = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)

def hash_password(raw: str) -> str:
    return _pwd_ctx.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    return _pwd_ctx.verify(raw, hashed)

def bootstrap_roles(db):
    existing_roles = db.execute(select(Role)).scalars().all()
    existing_role_names = {role.name for role in existing_roles}

    for role_name in RolePermissionConfig._roles:
        permissions = RolePermissionConfig.get_role_permissions(role_name)
        if role_name not in existing_role_names:
            # add roles which dont exist yet
            # permissions added later
            new_role = Role(
                name=role_name
            )
            db.add(new_role)
            db.commit()
            db.refresh(new_role)
            log_action(db, "role", new_role.id, "CREATE")
            print(f"[bold green]Created role[/bold green] {role_name}")

            for p in permissions:
                role_permission = RolePermission(
                    role_id=new_role.id,
                    permission=p.value
                )
                db.add(role_permission)
                print(f"  [bold green]+[/bold green] {p.name} (\"{p.value}\")")
            db.commit()
        else:
            # updated role permissions if changed
            role = db.execute(select(Role).where(Role.name == role_name)).scalars().first()
            current_permissions = {rp.permission for rp in role.role_permissions}
            new_permissions = {p.value for p in permissions}

            if current_permissions != new_permissions:
                print(f"[bold yellow]Updating role permissions[/bold yellow] {role_name}")
                # delete old permissions, should(?) be able to do delete inplace
                db.query(RolePermission).filter(RolePermission.role_id == role.id).delete()
                for p in permissions:
                    db.add(RolePermission(role_id=role.id, permission=p.value))
                    print(f"  ↪[bold green]+[/bold green] {p.name} (\"{p.value}\")")
                db.commit()
                log_action(db, "role", role.id, "UPDATE_PERMISSIONS")


def bootstrap_admin(db):
    # creates a manager if none exist yet, so its possible to test / login first time
    user_repo = UserRepository(db)
    mgr_repo = ManagerRepository(db)

    # does any user exist already?
    exists = db.execute(select(User.id)).first()
    if exists:
        return  # already bootstrapped

    # create a manager row for this person
    m = Manager(
        display_name="Admin",
        phone=None,
        email="admin@example.com",
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    log_action(db, "manager", m.id, "CREATE")

    # create the user row linked to that manager
    u = User(
        username="admin",
        password_hash=hash_password("admin12345"), 
        is_manager=True,
        is_active=True,
        role_id=db.execute(select(Role).where(Role.name == "ADMIN")).scalars().first().id,
        manager_id=m.id,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    log_action(db, "user", u.id, "CREATE")