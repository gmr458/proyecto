from datetime import datetime
from pydantic import BaseModel, EmailStr, constr


class UsuarioBaseSchema(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    email: EmailStr
    numero_documento: str
    perfil_id: int


class CreateUsuarioSchema(UsuarioBaseSchema):
    contrasena: str = constr(min_length=8)


class ResponseUsuarioSchema(UsuarioBaseSchema):
    id: int
    fecha_creacion: datetime
    activado: bool


class Usuario(UsuarioBaseSchema):
    id: int
    fecha_creacion: datetime
    activado: bool
    contrasena: str


class LoginUsuarioSchema(BaseModel):
    email: EmailStr
    contrasena: str = constr(min_length=8)
