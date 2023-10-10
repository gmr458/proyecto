from app.config.database import get_mysql_connection
from app.models.usuario import CreateUsuarioSchema


class UsuarioController:
    def create(self, usuario: CreateUsuarioSchema):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """INSERT INTO `usuario` (
                        `nombre`,
                        `apellido`,
                        `telefono`,
                        `email`,
                        `contrasena`,
                        `numero_documento`,
                        `activado`
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(
                        query,
                        (
                            usuario.nombre,
                            usuario.apellido,
                            usuario.telefono,
                            usuario.email,
                            usuario.contrasena,
                            usuario.numero_documento,
                            True,
                        ),
                    )
                connection.commit()
        except Exception as e:
            raise e

    def get_by_id(self, id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM `usuario` WHERE `id` = %s"
                    cursor.execute(query, (id,))
                    usuario = cursor.fetchone()
                    return usuario
        except Exception as e:
            raise e

    def get_by_email(self, email: str):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM `usuario` WHERE `email` = %s"
                    cursor.execute(query, (email,))
                    usuario = cursor.fetchone()
                    return usuario
        except Exception as e:
            raise e

    def get_by_numero_documento(self, numero_documento: str):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM `usuario` WHERE `numero_documento` = %s"
                    cursor.execute(query, (numero_documento,))
                    usuario = cursor.fetchone()
                    return usuario
        except Exception as e:
            raise e

    def get_by_telefono(self, telefono: str):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """SELECT * FROM `usuario` WHERE `telefono` = %s"""
                    cursor.execute(query, (telefono,))
                    usuario = cursor.fetchone()
                    return usuario
        except Exception as e:
            raise e
