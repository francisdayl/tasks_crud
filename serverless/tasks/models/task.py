import os
from datetime import datetime, timezone
from bson import ObjectId

from dotenv import load_dotenv

from config.db import connect_db
from tasks.enums.status import Status

load_dotenv()

db = connect_db()
TASKS_COLLECTION = os.getenv("TASKS_COLLECTION", "")
collection = db[TASKS_COLLECTION]


def cast_object_id_to_str(obj):
    if not obj:
        return None
    obj["id"] = str(obj.pop("_id"))
    obj["created_at"] = obj.pop("created_at").isoformat()
    obj["updated_at"] = obj.pop("updated_at").isoformat()
    if "user_id" in obj:
        obj["user_id"] = str(obj.pop("user_id"))
    return obj


class Task:
    @staticmethod
    def create(title: str, description: str, user_id: str):
        task = {
            "title": title,
            "description": description,
            "status": Status.IN_PROGRESS,
            "user_id": ObjectId(user_id),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = collection.insert_one(task)
        return str(result.inserted_id)

    @staticmethod
    def find_all():
        tasks = list(collection.find())
        if tasks:
            tasks = [cast_object_id_to_str(task) for task in tasks]
        return tasks

    @staticmethod
    def find_by_user(user_id: str):
        tasks = list(collection.find({"user_id": ObjectId(user_id)}))
        if tasks:
            tasks = [cast_object_id_to_str(task) for task in tasks]
        return tasks

    @staticmethod
    def find_by_id(task_id: str):
        task = collection.find_one({"_id": ObjectId(task_id)})
        if task:
            task = cast_object_id_to_str(task)
        return task

    @staticmethod
    def update(task_id: str, data):
        if "id" in data:
            del data["id"]
        data["updated_at"] = datetime.now(timezone.utc)
        result = collection.update_one({"_id": ObjectId(task_id)}, {"$set": data})
        return result.modified_count

    @staticmethod
    def delete(task_id: str):
        return collection.delete_one({"_id": ObjectId(task_id)})
