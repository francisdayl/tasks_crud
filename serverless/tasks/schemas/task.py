from pydantic import BaseModel

from tasks.enums.status import Status


class TaskSchema(BaseModel):
    title: str
    description: str
    status: Status
