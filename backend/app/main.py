from app.models.role import Permissions
from app.repositories.cat_procedure_repository import CatProcedureRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.procedure import ProcedureCreate, ProcedureRead
from app.schemas.task import TaskCreate, TaskRead
from app.services.procedure_service import ProcedureService
from app.services.task_service import TaskService
from fastapi import FastAPI, Depends, UploadFile, File, Form, Request, HTTPException, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from typing import List
from contextlib import asynccontextmanager
import mimetypes
from minio import Minio

from app.db.base import Base
from app.db.session import SessionLocal, engine, get_db
from app.schemas.cats import CatCreate, CatRead, CatUpdate

from app.schemas.manager import ManagerCreate, ManagerRead
from app.schemas.foster_home import FosterHomeCreate, FosterHomeRead

from app.repositories.cat_repository import CatRepository
from app.repositories.manager_repository import ManagerRepository
from app.repositories.foster_home_repository import FosterHomeRepository
from app.services.cat_service import CatService
from app.services.manager_service import ManagerService
from app.services.foster_home_service import FosterHomeService
from app.models.manager import Manager
from app.models.foster_home import FosterHome
from app.models.cat_procedure import CatProcedure

# NEW IMPORTS FOR AUTH / USERS
from app.schemas.user import UserCreate, UserRead, LoginRequest, LoginResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_checks import require_user, require_manager, require_permission
from app.services.auth_service import bootstrap_admin, bootstrap_roles

# Response vars
# set to true when deployed (prob should do via env var later)
API_HTTPS = False

# MinIO 
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
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


# test
@app.get("/")
async def read_root():
    return {"Hello": "World"}


# AUTH / USERS 

@app.post("/login", response_model=LoginResponse)
def login(response: Response, payload: LoginRequest, db = Depends(get_db)):
    svc = UserService(UserRepository(db), ManagerRepository(db))
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

    return LoginResponse(success=True)

@app.post("/users/full-create", response_model=UserRead, status_code=201)
def create_user_full(payload: UserCreate, db = Depends(get_db), auth = Depends(require_permission(Permissions.USER_ADD))):
    # only managers can add new people
    svc = UserService(UserRepository(db), ManagerRepository(db))
    new_user = svc.create_full_user(payload)
    return new_user


#  CATS !
@app.post("/cats", response_model=CatRead, status_code=201)
def create_cat(
    request: Request,
    db = Depends(get_db),
    auth = Depends(require_permission(Permissions.CAT_ADD)),
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
def list_cats(request: Request, db = Depends(get_db), auth = Depends(require_permission(Permissions.CAT_VIEW))):
    service = CatService(CatRepository(db), request.app.state.minio)
    return service.list_all()

@app.get("/cats/{cat_id}", response_model=CatRead)
def get_cat(cat_id: int, request: Request, db = Depends(get_db), auth = Depends(require_permission(Permissions.CAT_VIEW))):
    service = CatService(CatRepository(db), request.app.state.minio)
    return service.get(cat_id)

@app.patch("/cats/{cat_id}", response_model=CatRead)
def update_cat(
    cat_id: int,
    request: Request,
    db = Depends(get_db),
    auth = Depends(require_permission(Permissions.CAT_EDIT)),
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
def delete_cat(cat_id: int, db = Depends(get_db), auth = Depends(require_permission(Permissions.CAT_REMOVE))):
    cat = CatRepository(db).get_with_related(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="cat not found")
    CatService(CatRepository(db), None).delete(cat)
    return 

# MANAGERS
@app.post("/managers", response_model=ManagerRead, status_code=201)
def create_manager(payload: ManagerCreate, db = Depends(get_db), auth = Depends(require_permission(Permissions.USER_ADD))):
    svc = ManagerService(ManagerRepository(db))
    m = svc.create(payload.display_name, payload.phone, payload.email)
    return m  # ORM to ManagerRead (maps the raw db data to json (as defined in schema))

@app.get("/managers", response_model=list[ManagerRead])
def list_managers(db = Depends(get_db), auth = Depends(require_permission(Permissions.USER_VIEW))):
    svc = ManagerService(ManagerRepository(db))
    rows = svc.list_all()
    return rows

# FOSTER HOMES
@app.post("/foster-homes", response_model=FosterHomeRead, status_code=201)
def create_foster_home(payload: FosterHomeCreate, db = Depends(get_db), auth = Depends(require_permission(Permissions.FOSTER_ADD))):
    svc = FosterHomeService(FosterHomeRepository(db))
    return svc.create(payload.name, payload.phone, payload.email, payload.address, payload.comments)# ORM -> FosterHomeRead

@app.get("/foster-homes", response_model=list[FosterHomeRead])
def list_foster_homes(db = Depends(get_db), auth = Depends(require_permission(Permissions.FOSTER_VIEW))):
    svc = FosterHomeService(FosterHomeRepository(db))
    rows = svc.list_all()
    return rows  # ORM TO FosterHomeRead 


# MINIO IMAGE/FILE
@app.get("/image/{object_name}")
def get_image(object_name: str, request: Request, auth = Depends(require_user)):
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
    db = Depends(get_db),
    auth = Depends(require_permission(Permissions.PROCEDURE_ADD)),
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
def list_procedures(cat_id: int, db = Depends(get_db), auth = Depends(require_permission(Permissions.PROCEDURE_VIEW))):
    svc = ProcedureService(CatProcedureRepository(db), CatRepository(db), None)
    return svc.list_for_cat(cat_id)


# TASKS (for calendar)
@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate, db = Depends(get_db), auth = Depends(require_permission(Permissions.TASK_ADD))):
    
    svc = TaskService(TaskRepository(db), CatRepository(db))
    return svc.add(
        cat_id=payload.cat_id,
        type_=payload.type,
        due_date=payload.due_date,
        notes=payload.notes,
    )

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(db = Depends(get_db), auth = Depends(require_permission(Permissions.TASK_VIEW))):
    # gives all tasks
    svc = TaskService(TaskRepository(db), CatRepository(db))
    return svc.list_all()

@app.get("/cats/{cat_id}/tasks", response_model=list[TaskRead])
def list_tasks_for_cat(cat_id: int, db = Depends(get_db), auth = Depends(require_permission([Permissions.CAT_VIEW, Permissions.PROCEDURE_VIEW]))):
    svc = TaskService(TaskRepository(db), CatRepository(db))
    return svc.list_by_cat(cat_id)
