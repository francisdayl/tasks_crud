import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app


def generate_token(user_id, email):
    """
    Generate a JWT token for the user.

    Args:
        user_id (str): The user's ID
        email (str): The user's email

    Returns:
        str: JWT token
    """
    # Token expiration time
    exp = datetime.now(timezone.utc) + timedelta(
        seconds=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES", 3600)
    )

    # Create the payload
    payload = {
        "exp": exp,
        "iat": datetime.now(timezone.utc),
        "sub": user_id,
        "email": email,
    }

    # Generate the token
    token = jwt.encode(
        payload, current_app.config.get("JWT_SECRET_KEY"), algorithm="HS256"
    )

    return token


def decode_token(token):
    """
    Decode and validate a JWT token.

    Args:
        token (str): The JWT token to decode

    Returns:
        dict: Decoded token payload or error information
    """
    try:
        # Decode the token
        payload = jwt.decode(
            token, current_app.config.get("JWT_SECRET_KEY"), algorithms=["HS256"]
        )

        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
