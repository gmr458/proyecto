from pydantic import BaseModel, constr


class ObservacionBaseSchema(BaseModel):
    creador_id: int | None
    contenido: str = constr(min_length=110)
