from __future__ import annotations

from sqlalchemy import select

from app.extensions import db
from app.models import User
from app.utils.errors import ConflictError, UnauthorizedError
from app.utils.security import hash_password, verify_password


class AuthService:
    def register(self, *, email: str, password: str) -> User:
        email_norm = email.strip().lower()
        if not email_norm or "@" not in email_norm:
            raise ConflictError("Invalid email")

        existing = db.session.execute(select(User).where(User.email == email_norm)).scalar_one_or_none()
        if existing:
            raise ConflictError("Email already registered")

        user = User(email=email_norm, password_hash=hash_password(password))
        db.session.add(user)
        db.session.commit()
        return user

    def authenticate(self, *, email: str, password: str) -> User:
        email_norm = email.strip().lower()
        user = db.session.execute(select(User).where(User.email == email_norm)).scalar_one_or_none()
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid credentials")
        return user

