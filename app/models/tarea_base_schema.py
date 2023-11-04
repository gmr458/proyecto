from datetime import datetime

from pydantic import BaseModel

from app.models.prioridad import Prioridad
from app.models.tipo import Tipo


class TareaBaseSchema(BaseModel):
    titulo: str
    prioridad: Prioridad
    tipo: Tipo
    empleado_id: int
    creador_id: int | None
    fecha_limite: datetime
    evidencia: str | None
