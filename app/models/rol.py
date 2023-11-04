from pydantic import BaseModel

from app.models.nombre_rol import NombreRol


class Rol(BaseModel):
    id: int
    nombre: NombreRol
    description: str | None
