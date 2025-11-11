from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
import jwt
from typing import Optional, Literal

from app.models.user import User
from app.models.account import Account
from app.models.role import RolePermissionConfig

from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository

from app.schemas.user import UserCreate
from app.services.auth_service import hash_password, verify_password
from app.utils.audit import log_action

# move to gitlab ci variables or wherever we deploy later idk
SECRET_KEY = "randomkey"        
ALGO = "HS256"
TOKEN_EXPIRE_MIN = 60 * 8       

class UserService:
    def __init__(self, account_repo: AccountRepository, user_repo: UserRepository, role_repo: RoleRepository):
        self.account_repo = account_repo
        self.user_repo = user_repo
        self.role_repo = role_repo

    def create_full_user(self, data: UserCreate) -> User:
        # is username unique?
        if self.user_repo.get_by_username(data.username.strip()) is not None:
            raise HTTPException(status_code=409, detail="username already taken")
        
        # todo: could add a pw check towards haveibeenpwned, not sure how needed that is (1 fetch call)

        # todo: send email with login details if pw isnt sent
        if data.password is None:
            raise HTTPException(status_code=400, detail="account needs a password")

        if data.role_id is not None:
            # do we have a role with given id?
            role = self.role_repo.get_by_id(data.role_id)
            if role is None:
                raise HTTPException(status_code=400, detail=f"role with id {data.role_id} does not exist")
        else:
            role = self.role_repo.get_by_name("SOCIAL_WORKER")
            if role is None:
                raise HTTPException(status_code=410, detail=f"server couldn't find social worker role")

        # make account
        account = Account(
            username=data.username.strip(),
            password_hash=hash_password(data.password)
        )
    
        # make user
        u = User(
            account=account,
            role_id=data.role_id,
            display_name=data.display_name,
            phone=data.phone,
            email=data.email
        )

        try:
            created_account = self.account_repo.create(account)
            created_user = self.user_repo.create(u)
        except Exception as e:
            raise HTTPException(status_code=409, detail=f"something went wrong during user creation: {e}")

        log_action(self.account_repo.db, "account", created_account.id, "CREATE")
        log_action(self.user_repo.db, "user", created_user.id, "CREATE")

        return created_user


    def authenticate_user(self, username: str, password: str) -> User:
        user = self.user_repo.get_by_username(username.strip())
        if user is None:
            raise HTTPException(status_code=401, detail="invalid credentials")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="account disabled")

        if not verify_password(password, user.account.password_hash):
            raise HTTPException(status_code=401, detail="invalid credentials")

        return user

    def create_access_token(self, user: User) -> str:
        expire_at = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MIN)

        payload = { # type: ignore
            "sub": str(user.id),            
            "role": user.role.id,  # used for permission checks
            "exp": expire_at,
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO) # type: ignore
        return token

    def list_users_by_role(
        self,
        role: Optional[Literal[
            RolePermissionConfig.Roles.ADMIN,
            RolePermissionConfig.Roles.MANAGER,
            RolePermissionConfig.Roles.SOCIAL_WORKER,
        ]] | None = None
    ) -> list[User]:
        return list(self.user_repo.get_by_role_name(role=role.value if role is not None else None))