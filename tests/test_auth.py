"""Tests for authentication endpoints and utilities."""

import json

from app.auth import (
    get_user_by_id,
    get_user_by_username,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    """Tests for password hashing utilities."""

    def test_hash_password_returns_string(self):
        hashed = hash_password("mysecretpassword")
        assert isinstance(hashed, str)
        assert hashed != "mysecretpassword"

    def test_verify_password_correct(self):
        hashed = hash_password("mysecretpassword")
        assert verify_password("mysecretpassword", hashed) is True

    def test_verify_password_incorrect(self):
        hashed = hash_password("mysecretpassword")
        assert verify_password("wrongpassword", hashed) is False


class TestUserRetrieval:
    """Tests for user retrieval functions."""

    def test_get_user_by_username_found(self, test_user):
        user = get_user_by_username("testuser")
        assert user is not None
        assert user.username == "testuser"

    def test_get_user_by_username_not_found(self):
        user = get_user_by_username("nonexistent")
        assert user is None

    def test_get_user_by_id_found(self, test_user):
        user = get_user_by_id(test_user.id)
        assert user is not None
        assert user.id == test_user.id

    def test_get_user_by_id_not_found(self):
        user = get_user_by_id(9999)
        assert user is None


class TestRegistration:
    """Tests for the user registration endpoint."""

    def test_register_success(self, client):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
        }
        response = client.post(
            "/api/v1/register",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "User registered successfully"
        assert data["user"]["username"] == "newuser"

    def test_register_duplicate_username(self, client, test_user):
        payload = {
            "username": "testuser",
            "email": "another@example.com",
            "password": "securepassword123",
        }
        response = client.post(
            "/api/v1/register",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 409
        assert "already exists" in response.get_json()["error"]

    def test_register_duplicate_email(self, client, test_user):
        payload = {
            "username": "anotheruser",
            "email": "test@example.com",
            "password": "securepassword123",
        }
        response = client.post(
            "/api/v1/register",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 409
        assert "already registered" in response.get_json()["error"]

    def test_register_validation_error(self, client):
        payload = {"username": "ab", "email": "not-an-email", "password": "short"}
        response = client.post(
            "/api/v1/register",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestLogin:
    """Tests for the user login endpoint."""

    def test_login_success(self, client, test_user):
        payload = {"username": "testuser", "password": "password123"}
        response = client.post(
            "/api/v1/login",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "access_token" in data
        assert data["token_type"] == "Bearer"

    def test_login_invalid_password(self, client, test_user):
        payload = {"username": "testuser", "password": "wrongpassword"}
        response = client.post(
            "/api/v1/login",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 401
        assert "Invalid" in response.get_json()["error"]

    def test_login_user_not_found(self, client):
        payload = {"username": "ghost", "password": "password123"}
        response = client.post(
            "/api/v1/login",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 401

    def test_login_validation_error(self, client):
        payload = {"username": ""}
        response = client.post(
            "/api/v1/login",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 400


class TestProtectedEndpoints:
    """Tests for JWT-protected endpoints."""

    def test_access_without_token(self, client):
        response = client.get("/api/v1/notes")
        assert response.status_code == 401

    def test_access_with_invalid_token(self, client):
        response = client.get(
            "/api/v1/notes",
            headers={"Authorization": "Bearer invalidtoken"},
        )
        assert response.status_code == 401
