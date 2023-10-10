from enum import Enum

from pydantic import BaseModel


class NombreRol(str, Enum):
    administrador = "administrador"
    empleado = "empleado"


class Rol(BaseModel):
    id: int
    nombre: NombreRol
    description: str | None
