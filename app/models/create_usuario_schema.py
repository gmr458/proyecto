from pydantic import constr

from app.models.usuario_base_schema import UsuarioBaseSchema


class CreateUsuarioSchema(UsuarioBaseSchema):
    contrasena: str = constr(min_length=8)
    rol_id: int
