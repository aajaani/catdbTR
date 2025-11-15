from rich import print
from sqlalchemy import select
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from app.models.role import Role, RolePermissionConfig, RolePermission
from app.models.user import User
from app.models.account import Account

from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository

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


def bootstrap_roles(db: Session):
    existing_roles = db.execute(select(Role)).scalars().all()
    existing_role_names = {role.name for role in existing_roles}

    for role in RolePermissionConfig.Roles:
        role_name = role.value
        permissions = RolePermissionConfig().get_role_permissions(role_name)

        if permissions is None:
            permissions = ( )

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

            if role is None:
                raise RuntimeError(f"Can't update { role_name } permissions, doesn't exist in database (should never happen)")

            current_permissions = {rp.permission for rp in role.role_permissions}
            new_permissions = {p.value for p in permissions}

            if current_permissions != new_permissions:
                print(f"[bold yellow]Updating role permissions[/bold yellow] {role_name}")
                # delete old permissions, should(?) be able to do delete inplace
                db.query(RolePermission).filter(RolePermission.role_id == role.id).delete()
                for p in permissions:
                    db.add(RolePermission(role_id=role.id, permission=p.value))
                    print(f"    [bold green] + [/bold green] {p.name} (\"{p.value}\")")
                db.commit()
                log_action(db, "role", role.id, "UPDATE_PERMISSIONS")


def bootstrap_admin(db: Session):
    # creates a manager if none exist yet, so its possible to test / login first time
    account_repo = AccountRepository(db)  # type: ignore
    user_repo = UserRepository(db)  # type: ignore
    role_repo = RoleRepository(db)  # type: ignore

    # does any user exist already?
    exists = db.execute(select(User.id)).first()
    if exists:
        return  # already bootstrapped

    admin_role = role_repo.get_admin_role()

    if admin_role is None:
        raise RuntimeError("couln't find admin role in setup")

    # would use UserService but circular imports aaaaaaaaaaaaaaaa

    account = Account(
        username="admin",
        password_hash=hash_password("admin12345")
    )

    # make user
    u = User(
        account=account,
        display_name="default admin",
        role_id=admin_role.id,
        email="fix@deploy.gg"

    )

    try:
        created_account = account_repo.create(account)
        created_user = user_repo.create(u)
    except Exception as e:
        raise RuntimeError(e)

    log_action(account_repo.db, "account", created_account.id, "CREATE")
    log_action(user_repo.db, "user", created_user.id, "CREATE")

    print(f"[bold green]+[/bold green] bootstrapped initial admin account")
    