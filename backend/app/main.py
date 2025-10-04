# app/main.py

from fastapi import FastAPI, Depends, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import ValidationError
from typing import List
from contextlib import asynccontextmanager
import mimetypes
from minio import Minio

# meie enda importid
from app.db.base import Base
from app.db.session import engine, get_db
from app.schemas.cats import CatCreate, CatRead

# NEW: import proper schemas for managers & foster homes
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

# ---------- MinIO seaded ----------
MINIO_ENDPOINT = "localhost:9000"      # docker-compose port
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_SECURE = False
MINIO_BUCKET = "tkk-cats"

# lifespan – käivitatakse rakenduse alguses ja lõpetamisel
@asynccontextmanager
async def lifespan(app: FastAPI):
    # teeb andmebaasi tabelid
    Base.metadata.create_all(bind=engine)

    # lisab MinIO kliendi app.state sisse
    app.state.minio = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE,
    )
    # kui bucketit pole, siis tehakse uus
    if not app.state.minio.bucket_exists(MINIO_BUCKET):
        app.state.minio.make_bucket(MINIO_BUCKET)
    yield

# FastAPI rakendus
app = FastAPI(lifespan=lifespan)


# ---------- TEST JUUR ----------
@app.get("/")
async def read_root():
    return {"Hello": "World"}


# ---------- KASSID ----------
@app.post("/cats", response_model=CatRead, status_code=201)
def create_cat(
    request: Request,
    db = Depends(get_db),
    payload: str = Form(...),                      # JSON-string
    primary_image: UploadFile | None = File(None), # valikuline fail
):
    # püüame JSON payloadi Pydantic skeemiks parsida
    try:
        data = CatCreate.model_validate_json(payload)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    service = CatService(CatRepository(db), request.app.state.minio)
    return service.create_from_payload(data, primary_image)

@app.get("/cats", response_model=list[CatRead])
def list_cats(request: Request, db = Depends(get_db)):
    service = CatService(CatRepository(db), request.app.state.minio)
    return service.list_all()

@app.get("/cats/{cat_id}", response_model=CatRead)
def get_cat(cat_id: int, request: Request, db = Depends(get_db)):
    service = CatService(CatRepository(db), request.app.state.minio)
    return service.get(cat_id)


# ---------- HALDAJAD ----------
# MINIMAL CHANGE: use ManagerCreate as input, ManagerRead as output
@app.post("/managers", response_model=ManagerRead, status_code=201)
def create_manager(payload: ManagerCreate, db = Depends(get_db)):
    svc = ManagerService(ManagerRepository(db))
    m = svc.create(payload.display_name, payload.phone, payload.email)
    return m  # Pydantic from_attributes -> ManagerRead

@app.get("/managers", response_model=list[ManagerRead])
def list_managers(db = Depends(get_db)):
    svc = ManagerService(ManagerRepository(db))
    rows = svc.list_all()
    return rows  # list[ORM] -> list[ManagerRead] (from_attributes)


# ---------- HOIUKODUD ----------
# MINIMAL CHANGE: use FosterHomeCreate as input, FosterHomeRead as output
@app.post("/foster-homes", response_model=FosterHomeRead, status_code=201)
def create_foster_home(payload: FosterHomeCreate, db = Depends(get_db)):
    svc = FosterHomeService(FosterHomeRepository(db))
    f = svc.create(payload.name, payload.phone, payload.email, payload.address, payload.comments)
    return f  # ORM -> FosterHomeRead

@app.get("/foster-homes", response_model=list[FosterHomeRead])
def list_foster_homes(db = Depends(get_db)):
    svc = FosterHomeService(FosterHomeRepository(db))
    rows = svc.list_all()
    return rows  # list[ORM] -> list[FosterHomeRead]


# ---------- PILDI/FILI SAADEVÕTT MINIOST ----------
@app.get("/image/{object_name}")
def get_image(object_name: str, request: Request):
    try:
        # võtab objekti MinIO-st
        obj = request.app.state.minio.get_object(MINIO_BUCKET, object_name)
        # arvutab faililaiendist content-type
        content_type = mimetypes.guess_type(object_name)[0] or "application/octet-stream"
        return StreamingResponse(obj, media_type=content_type)
    except Exception:
        raise HTTPException(status_code=404, detail="Object not found or not accessible")
