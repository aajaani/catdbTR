from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import SECRET_KEY, ALGO
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthUser(BaseModel):
    user_id: int
    is_manager: bool

def require_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> AuthUser:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid or expired token")

    user_id = int(decoded["sub"])
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)

    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="invalid user")

    return AuthUser(user_id=user_id, is_manager=user.is_manager)

def require_manager(auth: AuthUser = Depends(require_user)) -> AuthUser:
    if not auth.is_manager:
        raise HTTPException(status_code=403, detail="insufficient rights")
    return auth
