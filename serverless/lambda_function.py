import json
from config.logger import logging

from dotenv import load_dotenv

from controllers.tasks import TaskController

load_dotenv()


# Lambda Handler
def lambda_handler(event, context):
    logging.info("Incoming Request")
    logging.info(event)

    http_method = event.get("httpMethod")
    headers = event.get("headers", {})
    authorization = ""
    if headers:
        auth = headers.get("authorization", "")
        authorization = auth if auth else headers.get("Authorization", "")
    query_string_parameters = event.get("queryStringParameters", None)
    query_string_parameters = query_string_parameters if query_string_parameters else {}
    path = "/".join(event.get("path", "").split("/")[2:])

    controller_type = path.split("/")[0]

    body = event.get("body", {})
    if body:
        body = json.loads(body)

    response = {}
    if controller_type == "task" or controller_type == "tasks":
        response = TaskController.run_action(
            http_method=http_method,
            path=path,
            query_params=query_string_parameters,
            body=body,
            authorization=authorization,
        )
    else:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid Action"})}
    logging.info("Response")
    logging.info(response.to_dict())
    return response.to_json()


# lambda_handler(
#     {
#         "httpMethod": "POST",
#         "path": "/api/task",
#         "headers": {
#             "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJpZCI6IjY3ZTc5MTU1M2E5ZmQ2NjgyOTU4NDA4OCJ9.CcVQV5g4GIwVZmGxcTIuMpjDrrw-fIq6Fohrrfk5d4E"
#         },
#         "body": json.dumps(
#             {
#                 "title": "Entrevista",
#                 "description": "a las 3pm",
#                 "status": "En Progreso",
#             }
#         ),
#         # "queryStringParameters": {"user_id": "67e78cff11c295e40b557bcd"},
#     },
#     {},
# )
