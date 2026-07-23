"""Unit tests for model definitions and behavior."""

from app.models import Note, User


class TestUserModelUnit:
    """Unit tests for the User model."""

    def test_user_repr(self):
        user = User(id=1, username="alice", email="alice@example.com", password_hash="hash")
        assert repr(user) == "<User(id=1, username='alice')>"

    def test_user_attributes(self):
        user = User(
            username="bob",
            email="bob@example.com",
            password_hash="secret_hash",
        )
        assert user.username == "bob"
        assert user.email == "bob@example.com"
        assert user.password_hash == "secret_hash"


class TestNoteModelUnit:
    """Unit tests for the Note model."""

    def test_note_repr(self):
        note = Note(id=5, title="Shopping List", content="Milk, Eggs", owner_id=1)
        assert repr(note) == "<Note(id=5, title='Shopping List', owner_id=1)>"

    def test_note_attributes(self):
        note = Note(
            title="Meeting Notes",
            content="Discuss Q3 roadmap",
            owner_id=2,
        )
        assert note.title == "Meeting Notes"
        assert note.content == "Discuss Q3 roadmap"
        assert note.owner_id == 2
