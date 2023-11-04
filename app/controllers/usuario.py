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
                        `email`,
                        `contrasena`,
                        `numero_documento`,
                        `activado`
                    ) VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(
                        query,
                        (
                            usuario.nombre,
                            usuario.apellido,
                            usuario.email,
                            usuario.contrasena,
                            usuario.numero_documento,
                            True,
                        ),
                    )

                    user_id = cursor.lastrowid

                    cursor.execute(
                        """INSERT INTO `telefono` (
                            `usuario_id`,
                            `code_country`,
                            `number`
                        ) VALUES (%s, %s, %s)""",
                        (
                            user_id,
                            usuario.code_country,
                            usuario.phone_number,
                        ),
                    )
                    cursor.execute(
                        """INSERT INTO `roles_usuario` (
                            `usuario_id`,
                            `rol_id`
                        ) VALUES (%s, %s)""",
                        (
                            user_id,
                            usuario.rol_id,
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
                    query = """SELECT
                            usuario.`id`,
                            usuario.`nombre`,
                            usuario.`apellido`,
                            usuario.`email`,
                            usuario.`contrasena`,
                            usuario.`numero_documento`,
                            usuario.`fecha_creacion`,
                            usuario.`activado`,
                            telefono.`code_country`,
                            telefono.`number`
                        FROM `usuario`
                        INNER JOIN `telefono`
                            ON usuario.`id` = telefono.`usuario_id`
                        WHERE usuario.`id` = %s"""
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
                    query = """SELECT
                            usuario.`id`,
                            usuario.`nombre`,
                            usuario.`apellido`,
                            usuario.`email`,
                            usuario.`contrasena`,
                            usuario.`numero_documento`,
                            usuario.`fecha_creacion`,
                            usuario.`activado`,
                            telefono.`code_country`,
                            telefono.`number`
                        FROM `usuario`
                        INNER JOIN `telefono`
                            ON usuario.`id` = telefono.`usuario_id`
                        WHERE usuario.`email` = %s"""
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
                    query = """SELECT
                            usuario.`id`,
                            usuario.`nombre`,
                            usuario.`apellido`,
                            usuario.`email`,
                            usuario.`contrasena`,
                            usuario.`numero_documento`,
                            usuario.`fecha_creacion`,
                            usuario.`activado`,
                            telefono.`code_country`,
                            telefono.`number`
                        FROM `usuario`
                        INNER JOIN `telefono`
                            ON usuario.`id` = telefono.`usuario_id`
                        WHERE usuario.`numero_documento` = %s"""
                    cursor.execute(query, (numero_documento,))
                    usuario = cursor.fetchone()
                    return usuario
        except Exception as e:
            raise e

    def get_by_telefono(self, code_country: str, telefono: str):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """SELECT
                            usuario.`id`,
                            usuario.`nombre`,
                            usuario.`apellido`,
                            usuario.`email`,
                            usuario.`contrasena`,
                            usuario.`numero_documento`,
                            usuario.`fecha_creacion`,
                            usuario.`activado`,
                            telefono.`code_country`,
                            telefono.`number`
                        FROM `usuario`
                        INNER JOIN `telefono`
                            ON usuario.`id` = telefono.`usuario_id`
                        WHERE telefono.`code_country` = %s
                            AND telefono.`number` = %s"""
                    cursor.execute(
                        query,
                        (
                            code_country,
                            telefono,
                        ),
                    )
                    usuario = cursor.fetchone()
                    return usuario
        except Exception as e:
            raise e

    def get_all(self):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT
                            usuario.`id`,
                            usuario.`nombre`,
                            usuario.`apellido`,
                            usuario.`email`,
                            usuario.`contrasena`,
                            usuario.`numero_documento`,
                            usuario.`fecha_creacion`,
                            usuario.`activado`,
                            telefono.`code_country`,
                            telefono.`number`
                        FROM `usuario`
                        INNER JOIN `telefono`
                            ON usuario.`id` = telefono.`usuario_id`
                    """
                    cursor.execute(query)
                    usuarios = cursor.fetchall()
                    return usuarios
        except Exception as e:
            raise e

    def get_top_5_mas_tareas_ejecutadas(self):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT
                            usuario.id,
                            usuario.nombre,
                            usuario.apellido,
                            usuario.email,
                            usuario.numero_documento,
                            usuario.fecha_creacion,
                            usuario.activado,
                            telefono.code_country,
                            telefono.number,
                            COUNT(*) as tareas_ejecutadas
                        FROM usuario
                        LEFT JOIN tarea
                            ON usuario.id = tarea.empleado_id
                        LEFT JOIN telefono ON usuario.id = telefono.usuario_id
                        WHERE tarea.estado = 'ejecutada'
                        GROUP BY usuario.id, telefono.code_country, telefono.number
                        ORDER BY tareas_ejecutadas DESC
                        LIMIT 5
                    """
                    cursor.execute(query)
                    usuarios = cursor.fetchall()
                    return usuarios
        except Exception as e:
            raise e
