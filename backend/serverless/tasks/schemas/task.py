from pydantic import BaseModel

from enums.status import Status


class TaskSchema(BaseModel):
    title: str
    description: str
    status: Status
    user: str
