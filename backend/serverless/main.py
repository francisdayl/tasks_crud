import os
import json

import config.logger
import logging

from pydantic import BaseModel, Field
from enum import Enum
from dotenv import load_dotenv

from backend.app import Task

# Load environment variables
load_dotenv()


# Mock authentication middleware
def authenticate(event):
    headers = event.get("headers", {})
    auth_token = headers.get("Authorization")
    if not auth_token or auth_token != "Bearer valid_token":
        logging.error("Unauthorized request")
        return {"statusCode": 401, "body": json.dumps({"error": "Unauthorized"})}
    return None


# Lambda Handler
def lambda_handler(event, context):
    auth_error = authenticate(event)
    if auth_error:
        return auth_error

    http_method = event.get("httpMethod")
    path = event.get("pathParameters", {}).get("id")

    if http_method == "POST":
        return create_task(event)
    elif http_method == "GET" and path:
        return get_task(path)
    elif http_method == "PUT" and path:
        return update_task(event, path)
    elif http_method == "DELETE" and path:
        return delete_task(path)
    else:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid request"})}
