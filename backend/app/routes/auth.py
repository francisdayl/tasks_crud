from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user, validate_token

from app.utils.log_utils import log_response, log_request

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    summary: Register a new user with email and password
    parameters:
        - in: body
          name: user
          description: The user to create.
          schema:
            type: object
            required:
              - email
              - password
            properties:
              email:
                type: string
              password:
                type: string
    responses:
        201:
          description: Created
    """

    log_request(request)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    result, status_code = register_user(data)
    log_response(result)
    return jsonify(result), status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate user and returns the jwt
    ---
    tags:
      - Login
    parameters:
        - in: body
          name: user
          description: The user to create.
          schema:
            type: object
            required:
              - email
              - password
            properties:
              email:
                type: string
              password:
                type: string
    responses:
        200:
          description: OK
    """
    log_request(request)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    if "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    result, status_code = login_user(data.get("email"), data.get("password"))
    log_response(result)
    return jsonify(result), status_code


@auth_bp.route("/validate", methods=["GET"])
def validate():
    """
    Validates user token
    ---
    tags:
      - authenticate
    parameters:
        - in: header
          name: authorization
          type: string
          required: true
    responses:
        200:
          description: OK
    """
    log_request(request)
    """Validate a JWT token."""
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 401

    parts = auth_header.split()

    if parts[0].lower() != "bearer":
        return jsonify({"error": "Authorization header must start with Bearer"}), 401

    if len(parts) == 1:
        return jsonify({"error": "Token not found"}), 401

    if len(parts) > 2:
        return jsonify({"error": "Authorization header must be Bearer token"}), 401

    token = parts[1]
    result, status_code = validate_token(token)
    log_response(result)
    return jsonify(result), status_code
