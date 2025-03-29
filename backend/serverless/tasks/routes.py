import os
import json
import logging
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from ..config.db import connect_db

from .models.task import Task
from .schemas.task import TaskSchema

load_dotenv()

db = connect_db()
TASKS_COLLECTION = os.getenv("TASKS_COLLECTION", "")


collection = db[TASKS_COLLECTION]
# Create Task
def create_task(event):
    try:
        body = json.loads(event["body"])
        task = Task(**body)
        result = collection.insert_one(task.model_dump())
        return {"statusCode": 201, "body": json.dumps({"id": str(result.inserted_id)})}
    except Exception as e:
        logging.error(f"Error creating task: {e}")
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}


# Read Task
def get_task(task_id):
    task = collection.find_one({"_id": task_id})
    if task:
        task["id"] = str(task.pop("_id"))
        return {"statusCode": 200, "body": json.dumps(task)}
    return {"statusCode": 404, "body": json.dumps({"error": "Task not found"})}


# Update Task
def update_task(event, task_id):
    try:
        body = json.loads(event["body"])
        task = Task(**body)
        result = collection.update_one({"_id": task_id}, {"$set": task.model_dump()})
        if result.modified_count:
            return {"statusCode": 200, "body": json.dumps({"message": "Task updated"})}
        return {"statusCode": 404, "body": json.dumps({"error": "Task not found"})}
    except Exception as e:
        logging.error(f"Error updating task: {e}")
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}


# Delete Task
def delete_task(task_id):
    result = collection.delete_one({"_id": task_id})
    if result.deleted_count:
        return {"statusCode": 200, "body": json.dumps({"message": "Task deleted"})}
    return {"statusCode": 404, "body": json.dumps({"error": "Task not found"})}
