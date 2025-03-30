from flask import current_app
from app import mongo
from app.models.user import validate_user_data, create_user_document, serialize_user
from app.utils.password_utils import hash_password, check_password
from app.utils.jwt_utils import generate_token, decode_token


def register_user(user_data):
    """Register a new user in the system."""
    # Validate input data
    validated_data = validate_user_data(user_data)
    # If validation failed, return the errors
    if "errors" in validated_data:
        return validated_data

    email = user_data.get("email").lower()

    # Check if user already exists
    existing_user = mongo.db.users.find_one({"email": email})
    if existing_user:
        return {"error": "User with this email already exists"}, 409
    # Hash the password
    hashed_password = hash_password(user_data.get("password"))

    # Create user document
    user = create_user_document(email, hashed_password)

    # Insert into database
    mongo.db.users.insert_one(user)
    # Return user data (without password)
    return {
        "message": "User registered successfully",
        "user": serialize_user(user),
    }, 201


def login_user(email, password):
    """Authenticate a user and generate JWT token."""
    if not email or not password:
        return {"error": "Email and password are required"}, 400

    # Normalize email
    email = email.lower()

    # Find user by email
    user = mongo.db.users.find_one({"email": email})

    # Check if user exists and password is correct
    if not user or not check_password(password, user.get("password")):
        return {"error": "Invalid email or password"}, 401

    # Check if user is active
    if not user.get("is_active", False):
        return {"error": "Account is disabled"}, 403

    # Generate token
    token = generate_token(str(user.get("_id")), user.get("email"))

    return {
        "message": "Login successful",
        "user": serialize_user(user),
        "token": token,
        "expires_in": current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES"),
    }, 200


def validate_token(token):
    """Validate JWT token and return user info if valid."""
    # Decode and validate token
    decoded_token = decode_token(token)

    if "error" in decoded_token:
        return decoded_token, 401

    # Get user from database
    user = mongo.db.users.find_one({"email": decoded_token.get("email")})

    if not user:
        return {"error": "User not found"}, 404

    if not user.get("is_active", False):
        return {"error": "Account is disabled"}, 403

    return {"valid": True, "user": serialize_user(user)}, 200
