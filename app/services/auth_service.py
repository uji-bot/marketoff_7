from app.extensions import db
from app.models.admin_user import AdminUser


class AuthError(Exception):
    pass


def create_admin(username: str, password: str) -> AdminUser:
    username = username.strip()
    if not username:
        raise AuthError("Username is required")
    if not password or len(password) < 6:
        raise AuthError("Password must be at least 6 characters")

    if AdminUser.query.filter_by(username=username).first():
        raise AuthError(f"Username '{username}' already exists")

    admin = AdminUser(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    return admin


def authenticate(username: str, password: str) -> AdminUser | None:
    admin = AdminUser.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        return admin
    return None