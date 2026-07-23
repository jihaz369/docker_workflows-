import pytest

"""Tests for database operations and model integrity."""

from app.database import db
from app.models import Note, User


class TestDatabaseConnection:
    """Tests verifying database connectivity and ORM behavior."""

    def test_database_is_sqlite(self, app):
        assert "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]

    def test_tables_created(self, app):
        with app.app_context():
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            assert "users" in tables
            assert "notes" in tables


class TestUserModel:
    """Tests for the User database model."""

    def test_create_user(self, app):
        with app.app_context():
            user = User(
                username="dbtestuser",
                email="dbtest@example.com",
                password_hash="hashedpassword",
            )
            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.username == "dbtestuser"
            assert user.created_at is not None

    def test_user_unique_username(self, app):
        with app.app_context():
            user1 = User(
                username="uniqueuser",
                email="u1@example.com",
                password_hash="hash1",
            )
            db.session.add(user1)
            db.session.commit()

            user2 = User(
                username="uniqueuser",
                email="u2@example.com",
                password_hash="hash2",
            )
            db.session.add(user2)
            from sqlalchemy.exc import IntegrityError
            with pytest.raises(IntegrityError):
                db.session.commit()
            db.session.rollback()


class TestNoteModel:
    """Tests for the Note database model."""

    def test_create_note(self, app, test_user):
        with app.app_context():
            note = Note(
                title="Database Note",
                content="Created in DB test",
                owner_id=test_user.id,
            )
            db.session.add(note)
            db.session.commit()

            assert note.id is not None
            assert note.title == "Database Note"
            assert note.owner_id == test_user.id
            assert note.created_at is not None

    def test_note_cascade_delete(self, app, test_user):
        with app.app_context():
            note = Note(
                title="Cascade Test",
                content="Will be deleted with user",
                owner_id=test_user.id,
            )
            db.session.add(note)
            db.session.commit()

            db.session.delete(test_user)
            db.session.commit()

            remaining = db.session.execute(
                db.select(Note).where(Note.id == note.id)
            ).scalar_one_or_none()
            assert remaining is None

    def test_note_relationship(self, app, test_user):
        with app.app_context():
            note = Note(
                title="Relational Note",
                content="Testing relationships",
                owner_id=test_user.id,
            )
            db.session.add(note)
            db.session.commit()

            assert note.owner.username == "testuser"
            assert note in test_user.notes
