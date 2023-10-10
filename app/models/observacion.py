from datetime import datetime

from pydantic import BaseModel, constr


class ObservacionBaseSchema(BaseModel):
    contenido: str = constr(min_length=110)


class CreateObservacionSchema(ObservacionBaseSchema):
    pass


class Observacion(ObservacionBaseSchema):
    id: int
    tarea_id: int
    fecha_creacion: datetime
