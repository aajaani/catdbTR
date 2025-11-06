from fastapi import HTTPException
from datetime import datetime, timedelta
import jwt

from app.models.user import User
from app.models.manager import Manager
from app.repositories.user_repository import UserRepository
from app.repositories.manager_repository import ManagerRepository
from app.schemas.user import UserCreate
from app.services.auth_service import hash_password, verify_password
from app.utils.audit import log_action

# move to gitlab ci variables or wherever we deploy later idk
SECRET_KEY = "randomkey"        
ALGO = "HS256"
TOKEN_EXPIRE_MIN = 60 * 8       

class UserService:
    def __init__(self, user_repo: UserRepository, manager_repo: ManagerRepository):
        self.user_repo = user_repo
        self.manager_repo = manager_repo

    def create_full_user(self, data: UserCreate) -> User:
        # is username unique?
        if self.user_repo.get_by_username(data.username.strip()) is not None:
            raise HTTPException(status_code=409, detail="username already taken")

        # if this new person will manage cats / edit stuff,
        # we ALSO create a manager row for them for contact/assignment
        manager_id = None
        if data.is_manager:
            m = Manager(
                display_name=data.display_name.strip(),
                phone=data.phone,
                email=data.email,
            )
            self.manager_repo.db.add(m)
            self.manager_repo.db.commit()
            self.manager_repo.db.refresh(m)
            manager_id = m.id

            log_action(self.manager_repo.db, "manager", m.id, "CREATE")

        # now create the actual login user
        u = User(
            username=data.username.strip(),
            password_hash=hash_password(data.password),
            is_manager=data.is_manager,
            is_active=True,
            manager_id=manager_id,
        )
        u = self.user_repo.create(u)

        # audit log for user
        log_action(self.user_repo.db, "user", u.id, "CREATE")

        return u


    def authenticate_user(self, username: str, password: str) -> User:
        user = self.user_repo.get_by_username(username.strip())
        if user is None:
            raise HTTPException(status_code=401, detail="invalid credentials")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="account disabled")

        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="invalid credentials")

        return user

    def create_access_token(self, user: User) -> str:
        expire_at = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MIN)
        payload = {
            "sub": str(user.id),            
            "is_manager": user.is_manager,  # used for permission checks
            "exp": expire_at,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)
        return token
