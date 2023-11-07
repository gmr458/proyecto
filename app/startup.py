import os

from app.config.jwt import hash_password
from app.controllers.rol import RolController
from app.controllers.usuario import UsuarioController
from app.models.rol import NombreRol
from app.models.create_usuario_schema import CreateUsuarioSchema

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class UsuarioAdminNotFound(Exception):
    pass


class RolAdminNotFound(Exception):
    pass


def crear_usuario_admin():
    rol_controller = RolController()

    rol = rol_controller.get_by_nombre(NombreRol.administrador)
    if rol is None:
        raise RolAdminNotFound

    usuario = CreateUsuarioSchema(
        nombre=os.environ.get("ADMIN_NOMBRE", "Usuario"),
        apellido=os.environ.get("ADMIN_APELLIDO", "Admin"),
        code_country=os.environ.get("ADMIN_CODE_COUNTRY", "57"),
        phone_number=os.environ.get("ADMIN_NUMBER", "1234567890"),
        email=os.environ.get("ADMIN_EMAIL", "admin@email.com"),
        contrasena=os.environ.get("ADMIN_CONTRASENA", "admin123"),
        numero_documento=os.environ.get("ADMIN_NUM_DOC", "100200300400"),
        rol_id=rol["id"],
    )

    usuario_controller = UsuarioController()

    user_found = usuario_controller.get_by_email(usuario.email.lower())
    if user_found is not None:
        print("admin user already exists")
        return

    usuario.contrasena = hash_password(str(usuario.contrasena))
    usuario.email = usuario.email.lower()

    usuario_controller.create(usuario)
    print("admin user created")
