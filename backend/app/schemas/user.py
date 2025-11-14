from pydantic import BaseModel
from app.schemas.role import RoleRead

class UserUpdate(BaseModel):
    display_name: str | None
    role_id: int | None
    is_active: bool | None = None
    phone: str | None = None
    email: str | None = None


class UserCreate(BaseModel):
    username: str # account field, username to log in with
    password: str | None = None # account field, can be none to autocreate pw for account
    display_name: str
    phone: str | None = None
    email: str | None #cannot be null (but our right now configuration it has to be)
    role_id: int | None # role id to create with, if none supllied should default back to SocialWorker 


class UserRead(BaseModel):
    id: int
    
    display_name: str
    
    role: RoleRead

    is_active: bool
    phone: str | None
    email: str | None

    class ConfigDict:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    pass # removed bool for success, http status codes exist
