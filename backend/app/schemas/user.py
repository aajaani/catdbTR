from pydantic import BaseModel
from app.schemas.role import RoleRead


class UserCreate(BaseModel):
    username: str # account field, username to log in with
    password: str | None = None # account field, can be none to autocreate pw for account
    display_name: str
    phone: str | None = None
    email: str | None = None
    role_id: int | None # role id to create with, if none supllied should default back to SocialWorker 


class UserRead(BaseModel):
    id: int
    
    display_name: str
    
    role: RoleRead

    is_active: bool
    phone: str
    email: str

    class ConfigDict:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    pass # removed bool for success, http status codes exist
