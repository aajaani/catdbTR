from pydantic import BaseModel

class UserCreate(BaseModel):
    # uhh lot of overlap with managercreate, but when creating users, if the user is a manager, we need to create both entries
    username: str
    password: str
    display_name: str
    phone: str | None = None
    email: str | None = None
    is_manager: bool = False

class UserRead(BaseModel):
    id: int
    username: str
    is_manager: bool
    is_active: bool
    manager_id: int | None = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
