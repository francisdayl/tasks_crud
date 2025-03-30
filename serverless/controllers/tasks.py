import json
import re

from config.logger import logging


from tasks.routes import (
    create_task,
    get_task,
    get_tasks,
    get_user_tasks,
    update_task,
    delete_task,
)
from tasks.schemas.task import TaskSchema
from utils.request_validators import validate_query_params
from utils.auth_utils import get_user_id_from_auth
from utils.responseFormat import ResponseFormat


class TaskController:
    def __init__(self):
        pass

    @staticmethod
    def run_action(
        http_method: str, path: str, query_params, body, authorization
    ) -> ResponseFormat:
        if (
            http_method == "GET"
            and re.search("^tasks$", path)
            and validate_query_params(query_params, [])
        ):  # GET - /tasks
            response = ResponseFormat()
            try:
                data = get_tasks()
                response.body = {"data": data}
            except Exception as e:
                logging.error("Error on fetching tasks")
                response.status_code = 500
                response.body = {"error": "Error on database"}
            return response

        elif http_method == "GET" and re.search("^tasks/user$", path):  # GET - /tasks
            response = ResponseFormat()
            try:
                user_id = get_user_id_from_auth(authorization)
                data = get_user_tasks(user_id)
                response.body = {"data": data}
            except Exception as e:
                logging.error("Error on fetching tasks")
                response.status_code = 500
                response.body = {"error": "Error on database"}
            return response

        elif (
            http_method == "POST"
            and re.search("^task$", path)
            and validate_query_params(query_params, [])
        ):  # POST - /task
            response = ResponseFormat()
            try:
                tarea = TaskSchema(**body)
            except Exception as e:
                logging.error(str(e))
                response.status_code = 401
                response.body = {"error": "Invalid request body"}
                return response

            try:
                user_id = get_user_id_from_auth(authorization)
                data = create_task(user_id, tarea.model_dump())
                response.status_code = 201
                response.body = {"data": data}
            except Exception as e:
                logging.error("Error creating the task")
                response.status_code = 500
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
                if data:
                    response.status_code = 200
                    response.body = {"data": data}
                else:
                    logging.error("Task not found")
                    response.status_code = 404
                    response.body = {"error": "Task not found"}
            except Exception as e:
                logging.error("Error on fetching the data")
                response.status_code = 500
                response.body = {"error": "Error on database"}
            return response

        elif (
            http_method == "PUT"
            and re.search("^task$", path)
            and validate_query_params(query_params, ["id"])
        ):  # PUT /task?id={id}
            response = ResponseFormat()
            try:
                tarea = TaskSchema(**body)
            except Exception as e:
                logging.error(str(e))
                response.status_code = 401
                response.body = {"error": "Invalid request body"}
                return response

            try:
                data = update_task(query_params["id"], tarea.model_dump(mode="json"))
                if data > 0:
                    response.status_code = 203
                    response.body = {"message": "Task updated succesfully"}
                else:
                    response.status_code = 500
                    response.body = {"error": "Error while updating task"}
            except Exception as e:
                logging.error(f"Task not found")
                response.status_code = 404
                response.body = {"error": "Task not found"}
            return response

        elif (
            http_method == "DELETE"
            and re.search("^task$", path)
            and validate_query_params(query_params, ["id"])
        ):  # DELETE /task?id={id}
            response = ResponseFormat()
            try:
                data = delete_task(query_params["id"])
                if data:
                    response.status_code = 200
                    response.body = {"message": "Task deleted successfully"}
                else:
                    logging.error(f"Task not found")
                    response.status_code = 404
                    response.body = {"error": "Task Not Found"}
            except Exception as e:
                logging.error(f"Error on database")
                response.status_code = 500
                response.body = {"error": "Database error"}
            return response
        else:
            logging.error(f"Invalid request")
            response = ResponseFormat()
            response.status_code = 400
            response.body = {"error": "Invalid request"}
            return response
