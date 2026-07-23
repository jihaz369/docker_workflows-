"""Authentication utilities including password hashing and JWT handling."""

from functools import wraps
from typing import Any, Callable

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db
from app.models import User


def hash_password(password: str) -> str:
    """Hash a plain-text password using Werkzeug."""
    return generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plain-text password against a stored hash."""
    return check_password_hash(password_hash, password)


def get_user_by_username(username: str) -> User | None:
    """Retrieve a user by their username."""
    return db.session.execute(
        db.select(User).where(User.username == username)
    ).scalar_one_or_none()


def get_user_by_id(user_id: int) -> User | None:
    """Retrieve a user by their primary key ID."""
    return db.session.execute(
        db.select(User).where(User.id == user_id)
    ).scalar_one_or_none()


def create_user(username: str, email: str, password: str) -> User:
    """Create a new user with a hashed password."""
    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


def authenticate_user(username: str, password: str) -> User | None:
    """Authenticate a user by username and password."""
    user = get_user_by_username(username)
    if user and verify_password(password, user.password_hash):
        return user
    return None


def jwt_required_custom(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Custom decorator that wraps jwt_required with consistent error handling."""

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception:
            return jsonify({"error": "Authentication required."}), 401

    return wrapper
