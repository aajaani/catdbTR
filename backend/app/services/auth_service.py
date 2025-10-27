
from sqlalchemy import select
from passlib.context import CryptContext
from fastapi import HTTPException

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
        manager_id=m.id,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    log_action(db, "user", u.id, "CREATE")
    
