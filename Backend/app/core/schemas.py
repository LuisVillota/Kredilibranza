from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FormData(BaseModel):
    nombre_completo: str = Field(..., min_length=1)
    cedula: str = Field(..., min_length=1)
    convenio: str = Field(..., min_length=1)
    telefono: str = Field(..., min_length=1)
    fecha_nacimiento: datetime
    politica_privacidad: bool


class Submission(BaseModel):
    id: str
    nombre_completo: str
    cedula: str
    convenio: str
    telefono: str
    fecha_nacimiento: datetime
    politica_privacidad: bool
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
