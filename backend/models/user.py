from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError


class User(BaseModel):
    id: str = ""
    name: str
    email: str
    password: str
