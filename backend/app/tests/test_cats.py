import io
import pytest
from typing import BinaryIO, Set

from fastapi import HTTPException, UploadFile
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker, Session

from app.db.base import Base
from app.models.account import Account
from app.models.user import User
from app.models.foster_home import FosterHome
from app.models.role import RolePermissionConfig

from app.repositories.cat_repository import CatRepository
from app.repositories.role_repository import RoleRepository

from app.schemas.cats import CatCreate, CatUpdate

from app.services.auth_service import bootstrap_roles
from app.services.cat_service import CatService

from app.models.audit_log import AuditLog


# fake minio client used in tests
class DummyMinio:
    def __init__(self):
        self.objects: Set[str] = set()

    def stat_object(self, bucket: str, object_name: str):
        # raise if object not present (simulates minio behavior)
        if object_name not in self.objects:
            raise Exception("not found")
        return object_name

    def put_object(self, bucket: str, object_name: str, fileobj: BinaryIO, size: int, content_type: str | None = None):
        # remember we "uploaded" it
        self.objects.add(object_name)
        return object_name


@pytest.fixture()
def service_and_db():
    # create a new in-memory sqlite db for each test 
    engine = create_engine("sqlite:///:memory:", future=True)

    # enable fks in sqlite (they are off by default)
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA foreign_keys=ON")

    # create tables 
    Base.metadata.create_all(bind=engine)

    # open a session to this engine
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = Session()

    # need roles for manager accounts
    bootstrap_roles(db)
    # clear role audit logs for tests
    db.execute(delete(AuditLog))

    # wire the service to this session and a dummy minio
    service = CatService(CatRepository(db), DummyMinio())  # type: ignore (dummy client)

    try:
        yield service, db
    finally:
        db.close()
        engine.dispose()


def test_create_cat_trims_name_and_logs(service_and_db: tuple[CatService, Session]):
    service, db = service_and_db

    created = service.create_from_payload(CatCreate(name="  Mjau  "), primary_image=None)

    assert created.id is not None
    assert created.name == "Mjau"

    logs = db.execute(select(AuditLog)).scalars().all()
    assert len(logs) == 1
    assert logs[0].action == "CREATE"
    assert logs[0].entity_id == created.id


def test_create_cat_requires_non_empty_name(service_and_db: tuple[CatService, Session]):
    service, _ = service_and_db

    payload = CatCreate(name="   ")

    with pytest.raises(HTTPException) as exc:
        service.create_from_payload(payload, primary_image=None)

    assert exc.value.status_code == 422


def test_list_all_returns_related(service_and_db: tuple[CatService, Session]):
    service, db = service_and_db

    rolerepo = RoleRepository(db)
    manager_role = rolerepo.get_by_name(RolePermissionConfig.Roles.MANAGER.value)

    assert manager_role != None

    # create related rows that cats can point to
    account = Account(
        username="bobmarley1945",
        password_hash="wedontcare"
    )

    user = User(
        display_name="bob",
        phone="123",
        email="bob@fazeclan.com",
        account=account,
        role=manager_role,
        role_id=manager_role.id
    )

    foster_home = FosterHome(name="dust 2", phone="321")

    db.add_all([account, user, foster_home])
    db.commit()
    db.refresh(account)
    db.refresh(user)
    db.refresh(foster_home)

    # create two cats; one linked to manager + foster home
    service.create_from_payload(
        CatCreate(name="yummi", manager_id=user.id, foster_home_id=foster_home.id),
        primary_image=None,
    )
    service.create_from_payload(CatCreate(name="Luna"), primary_image=None)

    # list should include both, and related objects should be loaded
    cats = service.list_all()
    assert {cat.name for cat in cats} == {"yummi", "Luna"}

    yummi = next(cat for cat in cats if cat.name == "yummi")
    assert yummi.manager.display_name == "bob"
    assert yummi.foster_home.name == "dust 2"


def test_update_cat_adds_primary_image_and_logs(service_and_db: tuple[CatService, Session], monkeypatch):
    service, db = service_and_db

    # create cat
    created = service.create_from_payload(CatCreate(name="Chili"), primary_image=None)

    # monkeypatch for fake upload
    def fake_upload(minio_client: DummyMinio, file: BinaryIO):
        fake_upload.called = True
        return "object-key.png"

    fake_upload.called = False
    monkeypatch.setattr("app.services.cat_service.upload_to_minio", fake_upload)

    # fake upload file
    upload = UploadFile(filename="cat.png", file=io.BytesIO(b"image-bytes"))

    # update notes and set primary image
    updated = service.update_from_payload(created.id, CatUpdate(notes="locked in"), upload)

    # verify minio upload was invoked and fields updated
    assert fake_upload.called is True
    assert updated.primary_photo_object == "object-key.png"
    assert updated.notes == "locked in"

    # verify an "UPDATE" audit row exists for this cat id
    update_logs = db.execute(
        select(AuditLog).where(AuditLog.entity_id == created.id, AuditLog.action == "UPDATE")
    ).scalars().all()
    assert len(update_logs) == 1
