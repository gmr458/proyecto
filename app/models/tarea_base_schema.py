from datetime import datetime

from pydantic import BaseModel
from app.models.estado import Estado

from app.models.prioridad import Prioridad


class TareaBaseSchema(BaseModel):
    titulo: str
    prioridad: Prioridad
    tipo_id: int
    empleado_id: int
    creador_id: int | None
    fecha_limite: datetime
    evidencia: str | None
    estado: Estado | None = Estado.sin_iniciar
