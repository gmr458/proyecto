from app.config.database import get_mysql_connection
from app.models.tarea_base_schema import TareaBaseSchema


class TareaController:
    def create(self, tarea: TareaBaseSchema):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """INSERT INTO tarea (
                        titulo,
                        prioridad,
                        tipo_id,
                        empleado_id,
                        creador_id,
                        fecha_limite,
                        evidencia
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(
                        query,
                        (
                            tarea.titulo,
                            tarea.prioridad,
                            tarea.tipo_id,
                            tarea.empleado_id,
                            tarea.creador_id,
                            tarea.fecha_limite,
                            tarea.evidencia,
                        ),
                    )
                connection.commit()
        except Exception as e:
            raise e

    def get_all(self):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT
                            tarea.id,
                            tarea.titulo,
                            tarea.prioridad,
                            tipo_tarea.id AS tipo_tarea_id,
                            tipo_tarea.nombre AS tipo_tarea,
                            tipo_tarea.descripcion AS tipo_tarea_descripcion,
                            empleado.id AS empleado_id,
                            empleado.email AS empleado_email,
                            empleado.nombre AS empleado_nombre,
                            empleado.apellido AS empleado_apellido,
                            creador.id AS creador_id,
                            creador.email AS creador_email,
                            creador.nombre AS creador_nombre,
                            creador.apellido AS creador_apellido,
                            tarea.fecha_creacion,
                            tarea.fecha_limite,
                            tarea.evidencia,
                            tarea.estado
                        FROM tarea
                        LEFT JOIN usuario empleado
                            ON empleado.id = tarea.empleado_id
                        LEFT JOIN usuario creador
                            ON creador.id = tarea.creador_id
                        LEFT JOIN tipo_tarea
                            ON tipo_tarea.id = tarea.tipo_id
                    """
                    cursor.execute(query)
                    tareas = cursor.fetchall()
                    return tareas
        except Exception as e:
            raise e

    def get_by_usuario_id(self, id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT
                            tarea.id,
                            tarea.titulo,
                            tarea.prioridad,
                            tipo_tarea.id AS tipo_tarea_id,
                            tipo_tarea.nombre AS tipo_tarea,
                            tipo_tarea.descripcion AS tipo_tarea_descripcion,
                            empleado.id AS empleado_id,
                            empleado.email AS empleado_email,
                            empleado.nombre AS empleado_nombre,
                            empleado.apellido AS empleado_apellido,
                            creador.id AS creador_id,
                            creador.email AS creador_email,
                            creador.nombre AS creador_nombre,
                            creador.apellido AS creador_apellido,
                            tarea.fecha_creacion,
                            tarea.fecha_limite,
                            tarea.evidencia,
                            tarea.estado
                        FROM tarea
                        LEFT JOIN usuario empleado
                            ON empleado.id = tarea.empleado_id
                        LEFT JOIN usuario creador
                            ON creador.id = tarea.creador_id
                        LEFT JOIN tipo_tarea
                            ON tipo_tarea.id = tarea.tipo_id
                        WHERE tarea.empleado_id = %s
                    """
                    cursor.execute(query, (id,))
                    tareas = cursor.fetchall()
                    return tareas
        except Exception as e:
            raise e

    def get_by_id(self, id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT
                            tarea.id,
                            tarea.titulo,
                            tarea.prioridad,
                            tipo_tarea.id AS tipo_tarea_id,
                            tipo_tarea.nombre AS tipo_tarea,
                            tipo_tarea.descripcion AS tipo_tarea_descripcion,
                            empleado.id AS empleado_id,
                            empleado.email AS empleado_email,
                            empleado.nombre AS empleado_nombre,
                            empleado.apellido AS empleado_apellido,
                            creador.id AS creador_id,
                            creador.email AS creador_email,
                            creador.nombre AS creador_nombre,
                            creador.apellido AS creador_apellido,
                            tarea.fecha_creacion,
                            tarea.fecha_limite,
                            tarea.evidencia,
                            tarea.estado
                        FROM tarea
                        LEFT JOIN usuario empleado
                            ON empleado.id = tarea.empleado_id
                        LEFT JOIN usuario creador
                            ON creador.id = tarea.creador_id
                        LEFT JOIN tipo_tarea
                            ON tipo_tarea.id = tarea.tipo_id
                        WHERE tarea.id = %s
                    """
                    cursor.execute(query, (id,))
                    tarea = cursor.fetchone()
                    return tarea
        except Exception as e:
            raise e

    def get_by_titulo(self, titulo: str):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT
                            tarea.id,
                            tarea.titulo,
                            tarea.prioridad,
                            tipo_tarea.id AS tipo_tarea_id,
                            tipo_tarea.nombre AS tipo_tarea,
                            tipo_tarea.descripcion AS tipo_tarea_descripcion,
                            empleado.id AS empleado_id,
                            empleado.email AS empleado_email,
                            empleado.nombre AS empleado_nombre,
                            empleado.apellido AS empleado_apellido,
                            creador.id AS creador_id,
                            creador.email AS creador_email,
                            creador.nombre AS creador_nombre,
                            creador.apellido AS creador_apellido,
                            tarea.fecha_creacion,
                            tarea.fecha_limite,
                            tarea.evidencia,
                            tarea.estado
                        FROM tarea
                        LEFT JOIN usuario empleado
                            ON empleado.id = tarea.empleado_id
                        LEFT JOIN usuario creador
                            ON creador.id = tarea.creador_id
                        LEFT JOIN tipo_tarea
                            ON tipo_tarea.id = tarea.tipo_id
                        WHERE tarea.titulo = %s
                    """
                    cursor.execute(query, (titulo,))
                    tarea = cursor.fetchone()
                    return tarea
        except Exception as e:
            raise e

    def get_count_all(self) -> int:
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT COUNT(*) total_tasks FROM `tarea`"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if result is None:
                        return 0
                    return result["total_tasks"]
        except Exception as e:
            raise e

    def get_count_sin_iniciar(self) -> int:
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT COUNT(*) tareas_sin_iniciar FROM `tarea` WHERE estado = 'sin_iniciar'"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if result is None:
                        return 0
                    return result["tareas_sin_iniciar"]
        except Exception as e:
            raise e

    def get_count_en_proceso(self) -> int:
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT COUNT(*) tareas_en_proceso FROM `tarea` WHERE estado = 'en_proceso'"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if result is None:
                        return 0
                    return result["tareas_en_proceso"]
        except Exception as e:
            raise e

    def get_count_ejecutadas(self) -> int:
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT COUNT(*) tareas_ejecutadas FROM `tarea` WHERE estado = 'ejecutada'"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if result is None:
                        return 0
                    return result["tareas_ejecutadas"]
        except Exception as e:
            raise e

    def update_by_id(self, id: int, tarea: TareaBaseSchema):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        UPDATE `tarea` 
                        SET
                            titulo = %s,
                            prioridad = %s,
                            tipo_id = %s,
                            empleado_id = %s,
                            fecha_limite = %s,
                            evidencia = %s,
                            estado = %s
                        WHERE `id` = %s
                    """
                    cursor.execute(
                        query,
                        (
                            tarea.titulo,
                            tarea.prioridad,
                            tarea.tipo_id,
                            tarea.empleado_id,
                            tarea.fecha_limite,
                            tarea.evidencia,
                            tarea.estado,
                            id,
                        ),
                    )
                connection.commit()
        except Exception as e:
            raise e

    def delete_by_id(self, id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "DELETE FROM `tarea` WHERE `id` = %s"
                    cursor.execute(query, (id,))
                connection.commit()
        except Exception as e:
            raise e
