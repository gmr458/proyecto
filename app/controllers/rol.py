from app.config.database import get_mysql_connection
from app.models.rol import Rol


class RolController:
    def create(self, rol: Rol):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """INSERT INTO `rol` (
                        `nombre`,
                        `descripcion`
                    ) VALUES (%s, %s)"""
                    cursor.execute(
                        query,
                        (
                            rol.nombre,
                            rol.description,
                        ),
                    )
                connection.commit()
        except Exception as e:
            raise e

    def create_para_usuario(self, rol_id: int, usuario_id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """INSERT INTO `roles_usuario` (
                        `usuario_id`,
                        `rol_id`
                    ) VALUES (%s, %s)"""
                    cursor.execute(
                        query,
                        (
                            usuario_id,
                            rol_id,
                        ),
                    )
                connection.commit()
        except Exception as e:
            raise e

    def get_by_user_id(self, user_id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT
                            rol.id,
                            rol.nombre,
                            rol.descripcion
                        FROM `rol` 
                        INNER JOIN `roles_usuario`
                            ON roles_usuario.`rol_id` = rol.`id`
                        INNER JOIN `usuario`
                            ON roles_usuario.`usuario_id` = usuario.`id`
                        WHERE usuario.`id` = %s
                    """
                    cursor.execute(query, (user_id,))
                    roles = cursor.fetchall()
                    return roles
        except Exception as e:
            raise e

    def get_by_nombre(self, nombre: str):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM `rol` WHERE `nombre` = %s"
                    cursor.execute(query, (nombre,))
                    rol = cursor.fetchone()
                    return rol
        except Exception as e:
            raise e

    def get_by_id(self, id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM `rol` WHERE `id` = %s"
                    cursor.execute(query, (id,))
                    rol = cursor.fetchone()
                    return rol
        except Exception as e:
            raise e
