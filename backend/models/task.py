from datetime import datetime
from enum import Enum
from pydantic import BaseModel, PositiveInt, ValidationError


class Status(str, Enum):
    PENDING = "Por Hacer"
    IN_PROGRESS = "En Progreso"
    COMPLETED = "Completada"


class Task(BaseModel):
    id: str = ""
    title: str
    description: str
    status: Status
    user: str
