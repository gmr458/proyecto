from pydantic import BaseModel, EmailStr


class UsuarioBaseSchema(BaseModel):
    nombre: str
    apellido: str
    code_country: str
    phone_number: str
    email: EmailStr
    numero_documento: str
