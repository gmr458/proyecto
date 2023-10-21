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


class Tipo(str, Enum):
    quimico = "quimico"
    agua = "agua"
    aire = "aire"
    reciclaje = "reciclaje"


class TareaBaseSchema(BaseModel):
    titulo: str
    prioridad: Prioridad
    tipo: Tipo
    empleado_id: int
    creador_id: int | None
    fecha_limite: datetime
    evidencia: str | None


class CreateTareaSchema(TareaBaseSchema):
    pass


class Tarea(TareaBaseSchema):
    id: int
    fecha_creacion: datetime
    estado: Estado = Estado.sin_iniciar
