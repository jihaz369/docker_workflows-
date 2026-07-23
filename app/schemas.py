"""Marshmallow schemas for request/response serialization."""

from marshmallow import Schema, fields, validate


class UserRegistrationSchema(Schema):
    """Schema for validating user registration requests."""

    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=80),
        metadata={"description": "Unique username (3-80 characters)"},
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=120),
        metadata={"description": "Valid email address"},
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128),
        load_only=True,
        metadata={"description": "Password (minimum 8 characters)"},
    )


class UserLoginSchema(Schema):
    """Schema for validating user login requests."""

    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=80),
        metadata={"description": "Registered username"},
    )
    password = fields.String(
        required=True,
        load_only=True,
        metadata={"description": "User password"},
    )


class UserResponseSchema(Schema):
    """Schema for serializing user data in responses."""

    id = fields.Integer(dump_only=True)
    username = fields.String()
    email = fields.Email()
    created_at = fields.DateTime(dump_only=True)


class NoteCreateSchema(Schema):
    """Schema for validating note creation requests."""

    title = fields.String(
        required=True,
        validate=validate.Length(min=1, max=200),
        metadata={"description": "Note title (1-200 characters)"},
    )
    content = fields.String(
        required=True,
        validate=validate.Length(min=1),
        metadata={"description": "Note content"},
    )


class NoteUpdateSchema(Schema):
    """Schema for validating note update requests."""

    title = fields.String(
        validate=validate.Length(min=1, max=200),
        metadata={"description": "Updated note title"},
    )
    content = fields.String(
        validate=validate.Length(min=1),
        metadata={"description": "Updated note content"},
    )


class NoteResponseSchema(Schema):
    """Schema for serializing note data in responses."""

    id = fields.Integer(dump_only=True)
    title = fields.String()
    content = fields.String()
    owner_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
