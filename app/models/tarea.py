from datetime import datetime

from app.models.estado import Estado
from app.models.tarea_base_schema import TareaBaseSchema


class Tarea(TareaBaseSchema):
    id: int
    fecha_creacion: datetime
