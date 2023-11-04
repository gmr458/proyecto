from pydantic import BaseModel, constr


class ObservacionBaseSchema(BaseModel):
    contenido: str = constr(min_length=110)
