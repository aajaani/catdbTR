from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
import jwt

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.role import Permissions
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.services.user_service import SECRET_KEY, ALGO
from pydantic import BaseModel

oauth2_scheme = APIKeyCookie(name="access_token")

class AuthUser(BaseModel):
    user_id: int
    permissions: list[Permissions]

def require_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> AuthUser:
    if not token:
        raise HTTPException(status_code=401, detail="missing token")

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])  # type: ignore
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid or expired token")

    user_id = int(decoded["sub"])
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)

    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="invalid user")

    role_repo = RoleRepository(db)
    role = role_repo.get_by_id(user.role_id)
    if role is None:
        raise HTTPException(status_code=401, detail="invalid user role")

    return AuthUser(
        user_id=user_id,
        permissions=[
            Permissions(rp.permission) for rp in role.role_permissions
        ]
    )


def require_permission(permissions: Permissions | list[Permissions]):
    if isinstance(permissions, Permissions):
        permissions = [permissions]

    def has_permission(auth: AuthUser = Depends(require_user)) -> bool:
        for permission in permissions:
            if not permission in auth.permissions:
                raise HTTPException(status_code=403, detail="insufficient rights")
        return True
    return has_permission

