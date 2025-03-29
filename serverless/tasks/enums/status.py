from enum import Enum


class Status(str, Enum):
    PENDING = "Por Hacer"
    IN_PROGRESS = "En Progreso"
    COMPLETED = "Completada"
