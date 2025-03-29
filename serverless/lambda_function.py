import json
from config.logger import logging

from dotenv import load_dotenv

from controllers.tasks import TaskController

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
    # auth_error = authenticate(event)
    # if auth_error:
    #     return auth_error

    http_method = event.get("httpMethod")
    query_string_parameters = event.get("queryStringParameters", {})
    path = event.get("path", "")[4:]
    body = json.loads(event["body"])
    controller_type = event.get("path").split("/")[1]
    if controller_type == "task" or controller_type == "tasks":
        return TaskController.run_action(
            http_method=http_method,
            path=path,
            query_params=query_string_parameters,
            body=body,
        )
    return {"statusCode": 400, "body": json.dumps({"error": "Invalid request"})}
