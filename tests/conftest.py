"""Pytest fixtures and configuration."""

import json

import pytest

from app.auth import hash_password
from app.database import db
from app.main import create_app
from app.models import User


@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Provide a test client for the application."""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create a standard test user in the database."""
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("password123"),
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture
def test_user2(app):
    """Create a second test user in the database."""
    with app.app_context():
        user = User(
            username="testuser2",
            email="test2@example.com",
            password_hash=hash_password("password456"),
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture
def auth_client(client, test_user):
    """Provide an authenticated test client with a valid JWT token."""
    response = client.post(
        "/api/v1/login",
        data=json.dumps({"username": "testuser", "password": "password123"}),
        content_type="application/json",
    )
    token = response.get_json()["access_token"]

    class AuthenticatedClient:
        def __init__(self, base_client, access_token):
            self.client = base_client
            self.token = access_token

        def get(self, url, **kwargs):
            headers = kwargs.pop("headers", {})
            headers["Authorization"] = f"Bearer {self.token}"
            return self.client.get(url, headers=headers, **kwargs)

        def post(self, url, **kwargs):
            headers = kwargs.pop("headers", {})
            headers["Authorization"] = f"Bearer {self.token}"
            return self.client.post(url, headers=headers, **kwargs)

        def put(self, url, **kwargs):
            headers = kwargs.pop("headers", {})
            headers["Authorization"] = f"Bearer {self.token}"
            return self.client.put(url, headers=headers, **kwargs)

        def delete(self, url, **kwargs):
            headers = kwargs.pop("headers", {})
            headers["Authorization"] = f"Bearer {self.token}"
            return self.client.delete(url, headers=headers, **kwargs)

    return AuthenticatedClient(client, token)
