from datetime import datetime, timezone
from marshmallow import Schema, fields, validate, ValidationError
from email_validator import validate_email, EmailNotValidError


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    created_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_only=True)


def validate_user_data(data):
    """Validate user data before creating or updating a user."""
    schema = UserSchema()
    try:
        validated_data = schema.load(data)
        # Additional email validation
        try:
            validate_email(data.get("email"))
        except EmailNotValidError:
            raise ValidationError({"email": ["Invalid email address"]})
        return validated_data
    except ValidationError as err:
        return {"errors": err.messages}, 422


def create_user_document(email, hashed_password):
    """Create a new user document."""
    return {
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now(timezone.utc),
        "is_active": True,
    }


def serialize_user(user):
    """Serialize user document to JSON without sensitive information."""
    if not user:
        return None

    return {
        "email": user.get("email"),
        "created_at": user.get("created_at"),
        "is_active": user.get("is_active"),
    }
