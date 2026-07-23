"""API route definitions for the notes application."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity
from marshmallow import ValidationError

from app.auth import (
    authenticate_user,
    create_user,
    get_user_by_id,
    get_user_by_username,
    jwt_required_custom,
)
from app.database import db
from app.models import Note, User
from app.schemas import (
    NoteCreateSchema,
    NoteResponseSchema,
    NoteUpdateSchema,
    UserLoginSchema,
    UserRegistrationSchema,
    UserResponseSchema,
)

api_bp = Blueprint("api", __name__)

user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
user_response_schema = UserResponseSchema()
note_create_schema = NoteCreateSchema()
note_update_schema = NoteUpdateSchema()
note_response_schema = NoteResponseSchema()


@api_bp.route("/health", methods=["GET"])
def health_check() -> tuple:
    """Return the health status of the API."""
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "python-notes-api",
                "version": "1.0.0",
            }
        ),
        200,
    )


@api_bp.route("/register", methods=["POST"])
def register() -> tuple:
    """Register a new user account."""
    try:
        data = user_registration_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    if get_user_by_username(data["username"]):
        return jsonify({"error": "Username already exists"}), 409

    existing_email = db.session.execute(
        db.select(User).where(User.email == data["email"])
    ).scalar_one_or_none()
    if existing_email:
        return jsonify({"error": "Email already registered"}), 409

    user = create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )

    return (
        jsonify(
            {
                "message": "User registered successfully",
                "user": user_response_schema.dump(user),
            }
        ),
        201,
    )


@api_bp.route("/login", methods=["POST"])
def login() -> tuple:
    """Authenticate a user and return a JWT access token."""
    try:
        data = user_login_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    user = authenticate_user(data["username"], data["password"])
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return (
        jsonify(
            {
                "message": "Login successful",
                "access_token": access_token,
                "token_type": "Bearer",
            }
        ),
        200,
    )


@api_bp.route("/notes", methods=["GET"])
@jwt_required_custom
def list_notes() -> tuple:
    """Retrieve all notes belonging to the authenticated user."""
    user_id = int(get_jwt_identity())
    notes = db.session.execute(
        db.select(Note).where(Note.owner_id == user_id).order_by(Note.created_at.desc())
    ).scalars().all()

    return jsonify({"notes": note_response_schema.dump(notes, many=True)}), 200


@api_bp.route("/notes/<int:note_id>", methods=["GET"])
@jwt_required_custom
def get_note(note_id: int) -> tuple:
    """Retrieve a specific note by ID."""
    user_id = int(get_jwt_identity())
    note = db.session.execute(
        db.select(Note).where(Note.id == note_id, Note.owner_id == user_id)
    ).scalar_one_or_none()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    return jsonify(note_response_schema.dump(note)), 200


@api_bp.route("/notes", methods=["POST"])
@jwt_required_custom
def create_note() -> tuple:
    """Create a new note for the authenticated user."""
    try:
        data = note_create_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    user_id = int(get_jwt_identity())
    note = Note(
        title=data["title"],
        content=data["content"],
        owner_id=user_id,
    )
    db.session.add(note)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Note created successfully",
                "note": note_response_schema.dump(note),
            }
        ),
        201,
    )


@api_bp.route("/notes/<int:note_id>", methods=["PUT"])
@jwt_required_custom
def update_note(note_id: int) -> tuple:
    """Update an existing note by ID."""
    try:
        data = note_update_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    user_id = int(get_jwt_identity())
    note = db.session.execute(
        db.select(Note).where(Note.id == note_id, Note.owner_id == user_id)
    ).scalar_one_or_none()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    if "title" in data:
        note.title = data["title"]
    if "content" in data:
        note.content = data["content"]

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Note updated successfully",
                "note": note_response_schema.dump(note),
            }
        ),
        200,
    )


@api_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required_custom
def delete_note(note_id: int) -> tuple:
    """Delete a note by ID."""
    user_id = int(get_jwt_identity())
    note = db.session.execute(
        db.select(Note).where(Note.id == note_id, Note.owner_id == user_id)
    ).scalar_one_or_none()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted successfully"}), 200
