import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.role import RolePermissionConfig
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.services.auth_service import bootstrap_roles
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from fastapi import HTTPException


@pytest.fixture()
def user_service():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = Session()

    bootstrap_roles(db)

    svc = UserService(
        account_repo=AccountRepository(db),
        user_repo=UserRepository(db),
        role_repo=RoleRepository(db),
    )

    try:
        yield svc, db
    finally:
        db.close()
        engine.dispose()


def test_create_full_user_defaults_to_social_worker(user_service):
    svc, db = user_service
    payload = UserCreate(
        username="alice",
        password="secret123",
        display_name="Alice",
        phone=None,
        email="alice@example.com",
        role_id=None,  # should default to SOCIAL_WORKER
    )

    user = svc.create_full_user(payload)

    assert user.id is not None
    assert user.role is not None
    assert user.role.name == RolePermissionConfig.Roles.SOCIAL_WORKER.value


def test_create_full_user_rejects_duplicate_username(user_service):
    svc, db = user_service

    first = UserCreate(
        username="bob",
        password="pw1",
        display_name="Bob",
        phone=None,
        email="bob@example.com",
        role_id=None,
    )
    svc.create_full_user(first)

    second = UserCreate(
        username="bob",  # same username
        password="pw2",
        display_name="Bobby",
        phone=None,
        email="bobby@example.com",
        role_id=None,
    )

    with pytest.raises(HTTPException) as exc:
        svc.create_full_user(second)

    assert exc.value.status_code == 409
