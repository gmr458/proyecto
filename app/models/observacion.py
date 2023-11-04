from datetime import datetime

from app.models.observacion_base_schema import ObservacionBaseSchema


class Observacion(ObservacionBaseSchema):
    id: int
    tarea_id: int
    fecha_creacion: datetime
