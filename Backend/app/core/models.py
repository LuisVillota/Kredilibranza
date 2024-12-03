import uuid
from typing import Optional

import pydantic
from pydantic import BaseModel


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Document(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=generate_uuid)
    content: str


class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    hashed_password: str
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
