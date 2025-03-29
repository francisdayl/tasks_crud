import json
import re


from tasks.routes import create_task, get_task, get_tasks, update_task, delete_task
from utils.request_validators import validate_query_params


class TaskController:
    def __init__(self):
        pass

    @staticmethod
    def run_action(http_method: str, path: str, query_params, body):
        if (
            http_method == "GET"
            and re.search("^tasks$", path)
            and validate_query_params(query_params, ["id"])
        ):
            return get_tasks()
        elif http_method == "POST" and re.search("^task$", path):
            return create_task(query_params, body)

        elif (
            http_method == "GET"
            and re.search("^task$", path)
            and validate_query_params(query_params, ["id"])
        ):
            return get_task(query_params, body)

        elif (
            http_method == "PUT"
            and re.search("^task$", path)
            and validate_query_params(query_params, ["id"])
        ):
            return update_task(query_params, body)

        elif http_method == "DELETE" and path:
            return delete_task(query_params, body)
        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid request"})}
