from .models.task import Task


# Create Task
def create_task(user_id, body):
    return Task.create(
        title=body["title"], description=body["description"], user_id=user_id
    )


# Read Task
def get_task(task_id: str):
    return Task.find_by_id(task_id)


# Read Tasks
def get_tasks():
    return Task.find_all()


def get_user_tasks(user_id):
    return Task.find_by_user(user_id)


# Update Task
def update_task(task_id, body):
    return Task.update(task_id, body)


# Delete Task
def delete_task(task_id):
    return Task.delete(task_id).deleted_count
