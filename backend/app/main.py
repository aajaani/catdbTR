from fastapi.openapi.utils import get_openapi

import os
import mimetypes

from fastapi import FastAPI, Depends, UploadFile, File, Form, Request, HTTPException, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import ValidationError
from contextlib import asynccontextmanager
from minio import Minio

from app.db.base import Base
from app.db.session import SessionLocal, engine, get_db

from app.models.role import Permissions, RolePermissionConfig
from app.models.foster_home import FosterHome
from app.models.cat_procedure import CatProcedure

from app.repositories.account_repository import AccountRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.cat_procedure_repository import CatProcedureRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.cat_repository import CatRepository
from app.repositories.colony_repository import ColonyRepository
from app.repositories.foster_home_repository import FosterHomeRepository

from app.schemas.user import UserCreate, UserRead, UserUpdate, LoginRequest, LoginResponse
from app.schemas.role import RoleRead
from app.schemas.procedure import ProcedureCreate, ProcedureRead
from app.schemas.task import TaskCreate, TaskRead
from app.schemas.cats import CatCreate, CatRead, CatUpdate
from app.schemas.colony import ColonyCreate, ColonyRead
from app.schemas.foster_home import FosterHomeCreate, FosterHomeRead, FosterHomeUpdate

from app.services.auth_checks import require_user, require_permission
from app.services.auth_service import bootstrap_admin, bootstrap_roles
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.services.procedure_service import ProcedureService
from app.services.task_service import TaskService
from app.services.cat_service import CatService
from app.services.colony_service import ColonyService
from app.services.foster_home_service import FosterHomeService

from app.services.email_service import send_email
import secrets 

# Response vars
# set to true when deployed (prob should do via env var later)
API_HTTPS = False


# MinIO 
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_SECURE = False
MINIO_BUCKET = "tkk-cats"

# lifespan – activates on startup and shutdown of the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # makes tables
    Base.metadata.create_all(bind=engine)

    # bootstrap first admin user if needed
    db = SessionLocal()

    try:
        bootstrap_roles(db)
        bootstrap_admin(db)
    finally:
        db.close()

    # adds minio client to app
    app.state.minio = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE,
    )
    # creates bucket if not exists
    if not app.state.minio.bucket_exists(MINIO_BUCKET):
        app.state.minio.make_bucket(MINIO_BUCKET)
    yield

# FastAPI app
app = FastAPI(lifespan=lifespan)

# allow fron to communicate with backend
# https://fastapi.tiangolo.com/tutorial/cors/?h=cors#use-corsmiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Since CatUpdate model is not referenced in any API route directly,
# FastAPI cannot detect the schema properly for docs and validation
# which causes CatUpdate to be missing from the OpenAPI schema
# (and missing from hey-api client generation)
#
# fix: we manually inject the schema into the OpenAPI definition
def openapi_inject():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(title="catdb-schema", version="temp_v1.0", routes=app.routes)
    default_schemas = openapi_schema.setdefault("components", {}).setdefault("schemas", {})
    default_schemas["CatCreate"] = CatCreate.model_json_schema()
    default_schemas["CatUpdate"] = CatUpdate.model_json_schema()

    def _make_permission_key(permission: str):
        parts = permission.split( ":" )
        assert len(parts) == 2
        return f"{parts[0].upper()}_{parts[1].upper()}"

    default_schemas["Permissions"] = {
        "title": "Permissions",
        "type": "object",
        "properties": {
            _make_permission_key(p): {
                "enum": [p],
                "type": "string",
                "title": p
            } for p in Permissions
        },
        "required": [_make_permission_key(p) for p in Permissions]
    }

    default_schemas["Roles"] = {
        "title": "Roles",
        "type": "object",
        "properties": {
            r: {
                "enum": [r],
                "type": "string",
                "title": r
            } for r in RolePermissionConfig.Roles
        },
        "required": [ r for r in RolePermissionConfig.Roles]
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = openapi_inject


# test
@app.get("/")
async def read_root():
    return {"Hello": "World"}


# AUTH / USERS 
@app.post("/login", response_model=LoginResponse)
def login(response: Response, payload: LoginRequest, db: Session = Depends(get_db)):
    svc = UserService(
        account_repo=AccountRepository(db),
        role_repo=RoleRepository(db),
        user_repo=UserRepository(db)
    )

    user = svc.authenticate_user(payload.username, payload.password)
    token = svc.create_access_token(user)

    # also refresh token later via http-only cookie
    response.set_cookie(
        "access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=API_HTTPS,
        max_age=3600,  # 1 hour
        path="/",
    )

    return LoginResponse( )


@app.post("/users/full-create", response_model=UserRead, status_code=201)
def create_user_full(
    payload: UserCreate,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.USER_ADD))
):
    # only managers can add new people
    svc = UserService(
        account_repo=AccountRepository(db),
        role_repo=RoleRepository(db),
        user_repo=UserRepository(db)
    )

    raw_password = payload.password
    if not raw_password:
        raw_password = secrets.token_urlsafe(10)
        payload.password = raw_password

    new_user = svc.create_full_user(payload)

    try: 
        send_email(
            to=new_user.email,
            subject="Tere tulemast Kassid Koju!",
            body=(
                f"Tere, {new_user.display_name}! \n\n "
                f"Sinu konto on loodud. \n\n"
                f"Kasutajanimi: {payload.username}\n"
                f"Parool: {raw_password}\n\n"
                "Esimesel sisselogimisel soovitame muuta oma parooli: {http://localhost:8081/login}"
            )

        )
    except Exception as e: 
        print("EMAIL ERROR", e)
        pass

    return new_user


# only users who can add new accounts can see all roles
@app.get("/roles", response_model=list[RoleRead], status_code=201)
def get_all_roles(
    request: Request,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.ROLE_VIEW))
):
    svc = RoleService(RoleRepository(db))
    return svc.list_roles()


@app.get("/permissions", response_model=dict[str, str], tags=["meta"], status_code=200)
def get_all_permissions(
    request: Request,
    auth: bool = Depends(require_user)
):
    return { p: p for p in Permissions.__members__ }

# higher lever "wrappers" for users
# routes for managers & social workers
@app.get( "/managers", response_model=list[UserRead], status_code=200)
def list_managers(
    request: Request,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.USER_VIEW))
):
    svc = UserService(
        account_repo=AccountRepository(db),
        user_repo=UserRepository(db),
        role_repo=RoleRepository(db)
    )

    return svc.list_users_by_role(
        role=RolePermissionConfig.Roles.MANAGER
    )

@app.get( "/users", response_model=list[UserRead], status_code=200)
def list_users(
    request: Request,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.USER_VIEW))
):
    svc = UserService(
        account_repo=AccountRepository(db),
        user_repo=UserRepository(db),
        role_repo=RoleRepository(db)
    )

    return svc.list_users_by_role(role=None)

@app.patch( "/users/{user_id}", response_model=UserRead, status_code=200 )
def edit_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.USER_EDIT))
):
    svc = UserService(
        account_repo=AccountRepository(db),
        user_repo=UserRepository(db),
        role_repo=RoleRepository(db)
    )

    return svc.update(user_id, data)

@app.delete("/users/{user_id}", status_code=200)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.USER_REMOVE))
):
    svc = UserService(
        account_repo=AccountRepository(db),
        user_repo=UserRepository(db),
        role_repo=RoleRepository(db)
    )

    svc.delete_user(user_id)

#  CATS !
@app.post("/cats", response_model=CatRead, status_code=201)
def create_cat(
    request: Request,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.CAT_ADD)),
    payload: str = Form(...),                      # JSON-string, form since multipart
    primary_image: UploadFile | None = File(None), # optional file
):
    # try to parse the JSON payload to pydantic model (as defined in schemas/cats.py)
    try:
        data = CatCreate.model_validate_json(payload)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # create service and call the method
    service = CatService(CatRepository(db), request.app.state.minio)
    return service.create_from_payload(data, primary_image)

@app.get("/cats", response_model=list[CatRead])
def list_cats(request: Request, db: Session = Depends(get_db), auth: bool = Depends(require_permission(Permissions.CAT_VIEW))):
    service = CatService(CatRepository(db), request.app.state.minio)
    return service.list_all()

@app.get("/cats/{cat_id}", response_model=CatRead)
def get_cat(cat_id: int, request: Request, db: Session = Depends(get_db), auth: bool = Depends(require_permission(Permissions.CAT_VIEW))):
    service = CatService(CatRepository(db), request.app.state.minio)
    return service.get(cat_id)

@app.patch("/cats/{cat_id}", response_model=CatRead)
def update_cat(
    cat_id: int,
    request: Request,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.CAT_EDIT)),
    payload: str = Form(...),                      # JSON-string, form since multipart
    primary_image: UploadFile | None = File(None), # optional file
):
    # try to parse the JSON payload to pydantic model (as defined in schemas/cats.py)
    try:
        data = CatUpdate.model_validate_json(payload)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # create service and call the method
    service = CatService(CatRepository(db), request.app.state.minio)
    return service.update_from_payload(cat_id, data, primary_image)

@app.delete("/cats/{cat_id}", status_code=204)
def delete_cat(cat_id: int, db: Session = Depends(get_db), auth: bool = Depends(require_permission(Permissions.CAT_REMOVE))):
    cat = CatRepository(db).get_with_related(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="cat not found")
    CatService(CatRepository(db), None).delete(cat)
    return 

# CAT COLONIES
@app.get("/colonies", status_code=200, response_model=list[ColonyRead])
def get_all_colonies(
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.COLONY_VIEW))
):
    svc = ColonyService(ColonyRepository(db))
    return svc.list_all()

@app.get("/colonies/{colony_id}", status_code=201, response_model=ColonyRead)
def get_colony(
    colony_id: int,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.COLONY_VIEW))
):
    svc = ColonyService(ColonyRepository(db))
    return svc.get_by_id(colony_id)

@app.post("/colonies", status_code=201, response_model=ColonyRead)
def create_colony(
    payload: ColonyCreate,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.COLONY_ADD))
):
    svc = ColonyService(ColonyRepository(db))
    return svc.create(payload)

# FOSTER HOMES
@app.post("/foster-homes", response_model=FosterHomeRead, status_code=201)
def create_foster_home(payload: FosterHomeCreate, db: Session = Depends(get_db), auth: bool = Depends(require_permission(Permissions.FOSTER_ADD))):
    svc = FosterHomeService(FosterHomeRepository(db))
    return svc.create(payload.name, payload.phone, payload.email, payload.address, payload.comments)# ORM -> FosterHomeRead

@app.get("/foster-homes", response_model=list[FosterHomeRead])
def list_foster_homes(db: Session = Depends(get_db), auth: bool = Depends(require_permission(Permissions.FOSTER_VIEW))):
    svc = FosterHomeService(FosterHomeRepository(db))
    rows = svc.list_all()
    return rows  # ORM TO FosterHomeRead

@app.patch("/foster-homes/{home_id}", response_model=FosterHomeRead)
def update_foster_home(
    home_id: int,
    data: FosterHomeUpdate,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.FOSTER_EDIT)),
):
    svc = FosterHomeService(FosterHomeRepository(db))
    return svc.update(home_id, data)


# MINIO IMAGE/FILE
@app.get("/image/{object_name}")
def get_image(object_name: str, request: Request, auth: bool = Depends(require_user)):
    try:
        # takes object from MinIO
        obj = request.app.state.minio.get_object(MINIO_BUCKET, object_name)
        # gets content-type from file extension
        content_type = mimetypes.guess_type(object_name)[0] or "application/octet-stream"
        return StreamingResponse(obj, media_type=content_type)
    except Exception:
        raise HTTPException(status_code=404, detail="Object not found or not accessible")
    

# PROCEDURES

@app.post("/cats/{cat_id}/procedures", response_model=ProcedureRead, status_code=201)
def add_procedure(
    cat_id: int,
    request: Request,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_permission(Permissions.PROCEDURE_ADD)),
    payload: str = Form(...),
    file: UploadFile | None = File(None),
):
    # pydantic validation
    try:
        data = ProcedureCreate.model_validate_json(payload)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    svc = ProcedureService(CatProcedureRepository(db), CatRepository(db), request.app.state.minio)
    return svc.add(
        cat_id=cat_id,
        type_=data.type,
        is_repeat=data.is_repeat,
        at_date=data.at_date,
        notes=data.notes,
        payment=data.payment,
        file=file,
    )

@app.get("/cats/{cat_id}/procedures", response_model=list[ProcedureRead])
def list_procedures(cat_id: int, db: Session = Depends(get_db), auth: bool = Depends(require_permission(Permissions.PROCEDURE_VIEW))):
    svc = ProcedureService(CatProcedureRepository(db), CatRepository(db), None)
    return svc.list_for_cat(cat_id)


# TASKS (for calendar)
@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), auth: bool = Depends(require_permission(Permissions.TASK_ADD))):
    
    svc = TaskService(TaskRepository(db), CatRepository(db))
    return svc.add(
        cat_id=payload.cat_id,
        type_=payload.type,
        due_date=payload.due_date,
        notes=payload.notes,
    )

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db), auth: bool = Depends(require_permission(Permissions.TASK_VIEW))):
    # gives all tasks
    svc = TaskService(TaskRepository(db), CatRepository(db))
    return svc.list_all()

@app.get("/cats/{cat_id}/tasks", response_model=list[TaskRead])
def list_tasks_for_cat(cat_id: int, db: Session = Depends(get_db), auth: bool = Depends(require_permission([Permissions.CAT_VIEW, Permissions.PROCEDURE_VIEW]))):
    svc = TaskService(TaskRepository(db), CatRepository(db))
    return svc.list_by_cat(cat_id)

