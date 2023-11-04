from pydantic import BaseModel, EmailStr, constr


class LoginUsuarioSchema(BaseModel):
    email: EmailStr
    contrasena: str = constr(min_length=8)
