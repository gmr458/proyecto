from app.config.database import get_mysql_connection
from app.models.create_usuario_schema import CreateUsuarioSchema


class UsuarioController:
    def create(self, usuario: CreateUsuarioSchema):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO usuario (
                            nombre,
                            apellido,
                            email,
                            contrasena,
                            numero_documento,
                            code_country,
                            phone_number,
                            activado
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            usuario.nombre,
                            usuario.apellido,
                            usuario.email,
                            usuario.contrasena,
                            usuario.numero_documento,
                            usuario.code_country,
                            usuario.phone_number,
                            True,
                        ),
                    )
                    user_id = cursor.lastrowid
                    cursor.execute(
                        """INSERT INTO roles_usuario (
                            usuario_id,
                            rol_id
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
                    query = """
                        SELECT
                            usuario.id,
                            usuario.nombre,
                            usuario.apellido,
                            usuario.email,
                            usuario.numero_documento,
                            usuario.code_country,
                            usuario.phone_number,
                            usuario.fecha_creacion,
                            usuario.activado,
                            GROUP_CONCAT(rol.nombre) AS roles
                        FROM usuario
                        JOIN roles_usuario
                            ON roles_usuario.usuario_id = usuario.id
                        JOIN rol
                            ON rol.id = roles_usuario.rol_id
                        WHERE 
                            usuario.eliminado = false
                            AND usuario.id = %s
                        GROUP BY usuario.id
                    """
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
                    query = """
                        SELECT
                            usuario.id,
                            usuario.nombre,
                            usuario.apellido,
                            usuario.email,
                            usuario.contrasena,
                            usuario.numero_documento,
                            usuario.code_country,
                            usuario.phone_number,
                            usuario.fecha_creacion,
                            usuario.activado,
                            GROUP_CONCAT(rol.nombre) AS roles
                        FROM usuario
                        JOIN roles_usuario
                            ON roles_usuario.usuario_id = usuario.id
                        JOIN rol
                            ON rol.id = roles_usuario.rol_id
                        WHERE 
                            usuario.eliminado = false
                            AND usuario.email = %s
                        GROUP BY usuario.id
                    """
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
                    query = """
                        SELECT
                            usuario.id,
                            usuario.nombre,
                            usuario.apellido,
                            usuario.email,
                            usuario.contrasena,
                            usuario.numero_documento,
                            usuario.code_country,
                            usuario.phone_number,
                            usuario.fecha_creacion,
                            usuario.activado,
                            GROUP_CONCAT(rol.nombre) AS roles
                        FROM usuario
                        JOIN roles_usuario
                            ON roles_usuario.usuario_id = usuario.id
                        JOIN rol
                            ON rol.id = roles_usuario.rol_id
                        WHERE 
                            usuario.eliminado = false
                            AND usuario.numero_documento = %s
                        GROUP BY usuario.id
                    """
                    cursor.execute(query, (numero_documento,))
                    usuario = cursor.fetchone()
                    return usuario
        except Exception as e:
            raise e

    def get_by_telefono(self, phone_number: str):
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
                            usuario.contrasena,
                            usuario.numero_documento,
                            usuario.code_country,
                            usuario.phone_number,
                            usuario.fecha_creacion,
                            usuario.activado,
                            GROUP_CONCAT(rol.nombre) AS roles
                        FROM usuario
                        JOIN roles_usuario
                            ON roles_usuario.usuario_id = usuario.id
                        JOIN rol
                            ON rol.id = roles_usuario.rol_id
                        WHERE 
                            usuario.eliminado = false
                            AND usuario.phone_number = %s
                        GROUP BY usuario.id
                    """
                    cursor.execute(query, (phone_number,))
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
                            usuario.id,
                            usuario.nombre,
                            usuario.apellido,
                            usuario.email,
                            usuario.numero_documento,
                            usuario.code_country,
                            usuario.phone_number,
                            usuario.fecha_creacion,
                            usuario.activado,
                            GROUP_CONCAT(rol.nombre) AS roles
                        FROM usuario
                        JOIN roles_usuario
                            ON roles_usuario.usuario_id = usuario.id
                        JOIN rol
                            ON rol.id = roles_usuario.rol_id
                        WHERE usuario.eliminado = false
                        GROUP BY usuario.email
                    """
                    cursor.execute(query)
                    usuarios = cursor.fetchall()
                    return usuarios
        except Exception as e:
            raise e

    def get_top_mas_tareas_ejecutadas(self):
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
                            usuario.code_country,
                            usuario.phone_number,
                            usuario.fecha_creacion,
                            usuario.activado,
                            COUNT(*) as tareas_ejecutadas
                        FROM usuario
                        LEFT JOIN tarea
                            ON usuario.id = tarea.empleado_id
                        WHERE 
                            usuario.eliminado = false
                            AND tarea.estado = 'ejecutada'
                        GROUP BY usuario.id
                        ORDER BY tareas_ejecutadas DESC
                    """
                    cursor.execute(query)
                    usuarios = cursor.fetchall()
                    return usuarios
        except Exception as e:
            raise e

    def get_top_mas_tareas_en_proceso(self):
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
                            usuario.code_country,
                            usuario.phone_number,
                            usuario.fecha_creacion,
                            usuario.activado,
                            COUNT(*) as tareas_en_proceso
                        FROM usuario
                        LEFT JOIN tarea
                            ON usuario.id = tarea.empleado_id
                        WHERE
                            usuario.eliminado = false
                            AND tarea.estado = 'en_proceso'
                        GROUP BY usuario.id
                        ORDER BY tareas_en_proceso DESC
                    """
                    cursor.execute(query)
                    usuarios = cursor.fetchall()
                    return usuarios
        except Exception as e:
            raise e

    def get_top_mas_tareas_sin_iniciar(self):
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
                            usuario.code_country,
                            usuario.phone_number,
                            usuario.fecha_creacion,
                            usuario.activado,
                            COUNT(*) as tareas_sin_iniciar
                        FROM usuario
                        LEFT JOIN tarea
                            ON usuario.id = tarea.empleado_id
                        WHERE 
                            usuario.eliminado = false
                            AND tarea.estado = 'sin_iniciar'
                        GROUP BY usuario.id
                        ORDER BY tareas_sin_iniciar DESC
                    """
                    cursor.execute(query)
                    usuarios = cursor.fetchall()
                    return usuarios
        except Exception as e:
            raise e

    def get_top_mas_tareas_asignadas(self):
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
                            usuario.code_country,
                            usuario.phone_number,
                            usuario.fecha_creacion,
                            usuario.activado,
                            COUNT(*) as tareas_asignadas
                        FROM usuario
                        LEFT JOIN tarea
                            ON usuario.id = tarea.empleado_id
                        WHERE 
                            usuario.eliminado = false
                            AND usuario.id = tarea.empleado_id
                        GROUP BY usuario.id
                        ORDER BY tareas_asignadas DESC
                    """
                    cursor.execute(query)
                    usuarios = cursor.fetchall()
                    return usuarios
        except Exception as e:
            raise e

    def get_count_admins(self) -> int:
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT COUNT(*) count_administradores
                        FROM (
                            SELECT usuario.id
                            FROM usuario
                            JOIN roles_usuario
                                ON roles_usuario.usuario_id = usuario.id
                            JOIN rol
                                ON rol.id = roles_usuario.rol_id
                            WHERE
                                usuario.eliminado = false
                                AND rol.nombre = 'administrador'
                            GROUP BY usuario.id
                        ) AS data;
                    """
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if result is None:
                        return 0
                    return result["count_administradores"]
        except Exception as e:
            raise e

    def is_admin_by_id(self, usuario_id: int) -> bool:
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT usuario.id
                        FROM usuario
                        JOIN roles_usuario
                            ON roles_usuario.usuario_id = usuario.id
                        JOIN rol
                            ON rol.id = roles_usuario.rol_id
                        WHERE
                            usuario.eliminado = false
                            AND rol.nombre = 'administrador'
                            AND usuario.id = %s
                        GROUP BY usuario.id
                    """
                    cursor.execute(query, (id,))
                    user = cursor.fetchone()
                    if user is None:
                        return False
                    return True
        except Exception as e:
            raise e

    def get_count_empleados(self):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT COUNT(*) count_empleados
                        FROM (
                            SELECT usuario.id
                            FROM usuario
                            JOIN roles_usuario
                                ON roles_usuario.usuario_id = usuario.id
                            JOIN rol
                                ON rol.id = roles_usuario.rol_id
                            WHERE
                                usuario.eliminado = false
                                AND rol.nombre = 'empleado'
                            GROUP BY usuario.id
                        ) AS data;
                    """
                    cursor.execute(query)
                connection.commit()
        except Exception as e:
            raise e

    def delete_by_id(self, id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        UPDATE usuario
                        SET eliminado = true
                        WHERE id = %s
                    """
                    cursor.execute(query, (id,))
                connection.commit()
        except Exception as e:
            raise e
