import pytest
from app.services.auth_service import create_admin, authenticate, AuthError


def test_create_admin(db_session):
    admin = create_admin("boss", "secret123")
    assert admin.id is not None
    assert admin.password_hash != "secret123"


def test_create_admin_short_password_raises(db_session):
    with pytest.raises(AuthError):
        create_admin("boss", "123")


def test_create_admin_duplicate_username_raises(db_session):
    create_admin("boss", "secret123")
    with pytest.raises(AuthError):
        create_admin("boss", "another123")


def test_authenticate_success(db_session):
    create_admin("boss", "secret123")
    admin = authenticate("boss", "secret123")
    assert admin is not None


def test_authenticate_wrong_password_fails(db_session):
    create_admin("boss", "secret123")
    admin = authenticate("boss", "wrongpass")
    assert admin is None