import json
from config.logger import logging

from dotenv import load_dotenv

from controllers.tasks import TaskController

# Load environment variables
load_dotenv()


# Mock authentication middleware
def authenticate(headers):
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
    headers = event.get("headers", {})
    query_string_parameters = event.get("queryStringParameters", {})
    path = "/".join(event.get("path", "").split("/")[2:])
    controller_type = path.split("/")[0]

    body = event.get("body", {})
    if body:
        body = json.loads(body)

    if controller_type == "task" or controller_type == "tasks":
        response = TaskController.run_action(
            http_method=http_method,
            path=path,
            query_params=query_string_parameters,
            body=body,
        )
        return response.to_json()
    return {"statusCode": 400, "body": json.dumps({"error": "Invalid request"})}
