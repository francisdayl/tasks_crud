# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]

from app.routes import auth, tasks

# backend/app/models/user.py
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from bson import ObjectId


class User:
    @staticmethod
    def create(email, password, name):
        user = {
            "email": email,
            "password": generate_password_hash(password),
            "name": name,
        }
        result = db.users.insert_one(user)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def check_password(user, password):
        return check_password_hash(user["password"], password)


# backend/app/models/task.py
from app import db
from bson import ObjectId
from datetime import datetime


class Task:
    @staticmethod
    def create(title, description, user_id):
        task = {
            "title": title,
            "description": description,
            "status": "pending",
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = db.tasks.insert_one(task)
        return str(result.inserted_id)

    @staticmethod
    def find_by_user(user_id):
        return list(db.tasks.find({"user_id": user_id}))

    @staticmethod
    def find_by_id(task_id):
        return db.tasks.find_one({"_id": ObjectId(task_id)})

    @staticmethod
    def update(task_id, data):
        data["updated_at"] = datetime.utcnow()
        db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": data})
        return Task.find_by_id(task_id)

    @staticmethod
    def delete(task_id):
        db.tasks.delete_one({"_id": ObjectId(task_id)})


# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, validator
import re


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    name: str

    @validator("password")
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


# backend/app/schemas/task.py
from pydantic import BaseModel, validator
from typing import Optional


class TaskCreateSchema(BaseModel):
    title: str
    description: str

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Title cannot be empty")
        if len(v) > 100:
            raise ValueError("Title must be less than 100 characters")
        return v

    @validator("description")
    def description_length(cls, v):
        if len(v) > 500:
            raise ValueError("Description must be less than 500 characters")
        return v


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

    @validator("status")
    def status_must_be_valid(cls, v):
        if v not in ["pending", "in_progress", "completed"]:
            raise ValueError("Status must be one of: pending, in_progress, completed")
        return v

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if v is not None:
            if not v or v.strip() == "":
                raise ValueError("Title cannot be empty")
            if len(v) > 100:
                raise ValueError("Title must be less than 100 characters")
        return v

    @validator("description")
    def description_length(cls, v):
        if v is not None and len(v) > 500:
            raise ValueError("Description must be less than 500 characters")
        return v


# backend/app/routes/auth.py
from flask import request, jsonify
from flask_pydantic import validate
from flask_jwt_extended import create_access_token
from app import app
from app.models.user import User
from app.schemas.user import UserRegisterSchema, UserLoginSchema
from bson.json_util import dumps
import json


@app.route("/api/auth/register", methods=["POST"])
@validate()
def register(body: UserRegisterSchema):
    # Check if user already exists
    existing_user = User.find_by_email(body.email)
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    # Create new user
    user_id = User.create(body.email, body.password, body.name)

    # Generate token
    access_token = create_access_token(identity=str(user_id))

    return (
        jsonify(
            {
                "access_token": access_token,
                "user": {"id": user_id, "email": body.email, "name": body.name},
            }
        ),
        201,
    )


@app.route("/api/auth/login", methods=["POST"])
@validate()
def login(body: UserLoginSchema):
    # Find user by email
    user = User.find_by_email(body.email)
    if not user or not User.check_password(user, body.password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate token
    access_token = create_access_token(identity=str(user["_id"]))

    return (
        jsonify(
            {
                "access_token": access_token,
                "user": {
                    "id": str(user["_id"]),
                    "email": user["email"],
                    "name": user["name"],
                },
            }
        ),
        200,
    )


# backend/app/routes/tasks.py
from flask import request, jsonify
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app
from app.models.task import Task
from app.schemas.task import TaskCreateSchema, TaskUpdateSchema
from bson.json_util import dumps
import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


@app.route("/api/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.find_by_user(user_id)

    # Convert ObjectId to string
    for task in tasks:
        task["_id"] = str(task["_id"])

    return jsonify(tasks), 200


@app.route("/api/tasks", methods=["POST"])
@jwt_required()
@validate()
def create_task(body: TaskCreateSchema):
    user_id = get_jwt_identity()
    task_id = Task.create(body.title, body.description, user_id)
    task = Task.find_by_id(task_id)

    # Convert ObjectId to string
    task["_id"] = str(task["_id"])

    return jsonify(task), 201


@app.route("/api/tasks/<task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.find_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if task["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    # Convert ObjectId to string
    task["_id"] = str(task["_id"])

    return jsonify(task), 200


@app.route("/api/tasks/<task_id>", methods=["PUT"])
@jwt_required()
@validate()
def update_task(task_id, body: TaskUpdateSchema):
    user_id = get_jwt_identity()
    task = Task.find_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if task["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    # Filter out None values
    update_data = {k: v for k, v in body.dict().items() if v is not None}

    updated_task = Task.update(task_id, update_data)

    # Convert ObjectId to string
    updated_task["_id"] = str(updated_task["_id"])

    return jsonify(updated_task), 200


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.find_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if task["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    Task.delete(task_id)

    return jsonify({"message": "Task deleted successfully"}), 200


# backend/run.py
from app import app

if __name__ == "__main__":
    app.run(debug=True)
