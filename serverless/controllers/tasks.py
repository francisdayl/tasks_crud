import json
import re


from tasks.routes import create_task, get_task, get_tasks, update_task, delete_task
from utils.request_validators import validate_query_params

from serverless.utils.responseFormat import ResponseFormat


class TaskController:
    def __init__(self):
        pass

    @staticmethod
    def run_action(http_method: str, path: str, query_params, body) -> ResponseFormat:
        if http_method == "GET" and re.search("^tasks$", path):  # GET - /tasks
            response = ResponseFormat()
            try:
                data = get_tasks()
                response.body = {"data": data}
            except Exception as e:
                response.status_code(500)
                response.body = {"error": "Error on database"}
            return response

        elif http_method == "POST" and re.search("^task$", path, body):  # POST - /task
            response = ResponseFormat()
            try:
                data = create_task(query_params, body)
                response.status_code = 201
                response.body = {"data": data}
            except Exception as e:
                response.status_code(500)
                response.body = {"error": "Error creating the task"}
            return response

        elif (
            http_method == "GET"
            and re.search("^task$", path)
            and validate_query_params(query_params, ["id"])
        ):  # GET /task?id={id}
            response = ResponseFormat()
            try:
                data = get_task(query_params["id"])
                response.status_code = 200
                response.body = {"data": data}
            except Exception as e:
                response.status_code(403)
                response.body = {"error": "Task not found"}
            return response

        elif (
            http_method == "PUT"
            and re.search("^task$", path)
            and validate_query_params(query_params, ["id"])
        ):  # PUT /task?id={id}
            response = ResponseFormat()
            try:
                data = update_task(query_params["id"])
                response.status_code = 203
                response.body = {"data": data}
            except Exception as e:
                response.status_code(403)
                response.body = {"error": "Task not found"}
            return response

        elif (
            http_method == "DELETE"
            and re.search("^task$", path)
            and validate_query_params(query_params, ["id"])
        ):  # DELETE /task?id={id}
            response = ResponseFormat()

            return delete_task(query_params, body)
        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid request"})}
