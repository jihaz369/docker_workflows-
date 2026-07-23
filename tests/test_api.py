"""Integration tests for the API endpoints."""

import json

import pytest

from app.database import db
from app.models import Note


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_200(self, client):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["service"] == "python-notes-api"


class TestNoteCRUD:
    """Integration tests for note CRUD operations."""

    def test_create_note(self, auth_client, test_user):
        payload = {"title": "My First Note", "content": "This is the content."}
        response = auth_client.post(
            "/api/v1/notes",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Note created successfully"
        assert data["note"]["title"] == "My First Note"
        assert data["note"]["owner_id"] == test_user.id

    def test_create_note_validation_error(self, auth_client):
        payload = {"title": "", "content": ""}
        response = auth_client.post(
            "/api/v1/notes",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_list_notes(self, auth_client, test_user):
        note = Note(title="Note 1", content="Content 1", owner_id=test_user.id)
        db.session.add(note)
        db.session.commit()

        response = auth_client.get("/api/v1/notes")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["notes"]) == 1
        assert data["notes"][0]["title"] == "Note 1"

    def test_list_notes_empty(self, auth_client):
        response = auth_client.get("/api/v1/notes")
        assert response.status_code == 200
        data = response.get_json()
        assert data["notes"] == []

    def test_get_note(self, auth_client, test_user):
        note = Note(title="Specific Note", content="Specific Content", owner_id=test_user.id)
        db.session.add(note)
        db.session.commit()

        response = auth_client.get(f"/api/v1/notes/{note.id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == "Specific Note"

    def test_get_note_not_found(self, auth_client):
        response = auth_client.get("/api/v1/notes/9999")
        assert response.status_code == 404
        data = response.get_json()
        assert data["error"] == "Note not found"

    def test_update_note(self, auth_client, test_user):
        note = Note(title="Old Title", content="Old Content", owner_id=test_user.id)
        db.session.add(note)
        db.session.commit()

        payload = {"title": "New Title", "content": "New Content"}
        response = auth_client.put(
            f"/api/v1/notes/{note.id}",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["note"]["title"] == "New Title"

    def test_update_note_not_found(self, auth_client):
        payload = {"title": "New Title", "content": "New Content"}
        response = auth_client.put(
            "/api/v1/notes/9999",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_delete_note(self, auth_client, test_user):
        note = Note(title="To Delete", content="Delete me", owner_id=test_user.id)
        db.session.add(note)
        db.session.commit()

        response = auth_client.delete(f"/api/v1/notes/{note.id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Note deleted successfully"

    def test_delete_note_not_found(self, auth_client):
        response = auth_client.delete("/api/v1/notes/9999")
        assert response.status_code == 404

    def test_note_isolation_between_users(self, client, test_user, test_user2):
        note = Note(title="Private", content="Private content", owner_id=test_user.id)
        db.session.add(note)
        db.session.commit()

        token_response = client.post(
            "/api/v1/login",
            data=json.dumps({"username": "testuser2", "password": "password456"}),
            content_type="application/json",
        )
        token = token_response.get_json()["access_token"]

        response = client.get(
            f"/api/v1/notes/{note.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
