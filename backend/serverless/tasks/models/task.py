from app import db
from bson import ObjectId
from datetime import datetime

from ..enums.status import Status


class Task:
    @staticmethod
    def create(title, description, user_id):
        task = {
            "title": title,
            "description": description,
            "status": Status.IN_PROGRESS,
            "user_id": user_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
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
        data["updated_at"] = datetime.now()
        db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": data})
        return Task.find_by_id(task_id)

    @staticmethod
    def delete(task_id):
        db.tasks.delete_one({"_id": ObjectId(task_id)})
