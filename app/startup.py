import os

from app.config.jwt import hash_password
from app.controllers.rol import RolController
from app.controllers.usuario import UsuarioController
from app.models.rol import NombreRol
from app.models.usuario import CreateUsuarioSchema


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
        telefono=os.environ.get("ADMIN_TELEFONO", "1234567890"),
        email=os.environ.get("ADMIN_EMAIL", "admin@email.com"),
        contrasena=os.environ.get("ADMIN_CONTRASENA", "admin123"),
        numero_documento=os.environ.get("ADMIN_NUM_DOC", "100200300400"),
        rol_id=rol["id"],
    )

    usuario_controller = UsuarioController()

    user_found = usuario_controller.get_by_email(usuario.email.lower())
    if user_found is not None:
        return

    usuario.contrasena = hash_password(str(usuario.contrasena))
    usuario.email = usuario.email.lower()

    usuario_controller.create(usuario)

    usuario_admin = usuario_controller.get_by_email(usuario.email)
    if usuario_admin is None:
        raise UsuarioAdminNotFound

    rol_controller.create_para_usuario(usuario.rol_id, usuario_admin["id"])
