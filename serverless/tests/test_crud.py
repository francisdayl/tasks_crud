import json
import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from lambda_function import lambda_handler
from tasks.models.task import collection

request_headers = {
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJpZCI6IjY3ZTc5MTU1M2E5ZmQ2NjgyOTU4NDA4OCJ9.CcVQV5g4GIwVZmGxcTIuMpjDrrw-fIq6Fohrrfk5d4E"
}


@pytest.fixture
def mock_mongo():
    """Fixture to mock MongoDB collection."""
    with patch("tasks.models.task.collection") as mock_collection:
        yield mock_collection


@pytest.fixture
def sample_task():
    return {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "En Progreso",
    }


@pytest.fixture
def sample_task_id():
    return str(ObjectId())


# Test Create Task
def test_create_task(mock_mongo, sample_task):
    mock_mongo.insert_one.return_value.inserted_id = ObjectId()
    event = {
        "httpMethod": "POST",
        "path": "/api/task",
        "headers": request_headers,
        "body": json.dumps(sample_task),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 201
    assert "data" in json.loads(response["body"])


# Test Get Task
def test_get_task(mock_mongo, sample_task, sample_task_id):
    mock_mongo.find_one.return_value = {"_id": ObjectId(sample_task_id), **sample_task}
    event = {"httpMethod": "GET", "path": "/api/tasks/user", "headers": request_headers}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    dict_response = json.loads(response["body"])["data"]
    assert type(dict_response) == list


# # Test Get Task Not Found
def test_get_task_not_found(mock_mongo, sample_task_id):
    mock_mongo.find_one.return_value = None
    event = {
        "httpMethod": "GET",
        "path": "/api/task",
        "headers": request_headers,
        "queryStringParameters": {"id": sample_task_id},
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 404


# Test Update Task
def test_update_task(mock_mongo, sample_task, sample_task_id):
    mock_mongo.update_one.return_value.modified_count = 1
    event = {
        "httpMethod": "PUT",
        "path": "/api/task",
        "headers": request_headers,
        "queryStringParameters": {"id": sample_task_id},
        "body": json.dumps(sample_task),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 203
    assert json.loads(response["body"])["message"] == "Task updated succesfully"


# Test Delete Task
def test_delete_task(mock_mongo, sample_task_id):
    mock_mongo.delete_one.return_value.deleted_count = 1
    event = {
        "httpMethod": "DELETE",
        "path": "/api/task",
        "headers": request_headers,
        "queryStringParameters": {"id": sample_task_id},
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["message"] == "Task deleted successfully"


# # Test Delete Task Not Found
def test_delete_task_not_found(mock_mongo, sample_task_id):
    mock_mongo.delete_one.return_value.deleted_count = 0
    event = {
        "httpMethod": "DELETE",
        "path": "/api/task",
        "headers": request_headers,
        "queryStringParameters": {"id": sample_task_id},
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 404
