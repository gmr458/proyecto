from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Prioridad(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"


class Estado(str, Enum):
    sin_iniciar = "sin_iniciar"
    en_proceso = "en_proceso"
    ejecutada = "ejecutada"


class TareaBaseSchema(BaseModel):
    titulo: str
    prioridad: Prioridad
    usuario_id: int
    fecha_limite: datetime
    evidencia: str | None


class CreateTareaSchema(TareaBaseSchema):
    pass


class Tarea(TareaBaseSchema):
    id: int
    fecha_creacion: datetime
    estado: Estado = Estado.sin_iniciar
