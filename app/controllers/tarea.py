from app.config.database import get_mysql_connection
from app.models.tarea import CreateTareaSchema


class TareaController:
    def create(self, tarea: CreateTareaSchema):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """INSERT INTO `tarea` (
                        `titulo`,
                        `prioridad`,
                        `tipo`,
                        `empleado_id`,
                        `creador_id`,
                        `fecha_limite`,
                        `evidencia`
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(
                        query,
                        (
                            tarea.titulo,
                            tarea.prioridad,
                            tarea.tipo,
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
                            t.id,
                            t.titulo,
                            t.prioridad,
                            t.tipo,
                            empleado.id AS empleado_id,
                            empleado.email AS empleado_email,
                            empleado.nombre AS empleado_nombre,
                            empleado.apellido AS empleado_apellido,
                            creador.id AS creador_id,
                            creador.email AS creador_email,
                            creador.nombre AS creador_nombre,
                            creador.apellido AS creador_apellido,
                            t.fecha_creacion,
                            t.fecha_limite,
                            t.evidencia,
                            t.estado
                        FROM tarea t
                        LEFT JOIN usuario empleado
                            ON empleado.id = t.empleado_id
                        LEFT JOIN usuario creador
                            ON creador.id = t.creador_id
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
                            t.id,
                            t.titulo,
                            t.prioridad,
                            t.tipo,
                            empleado.id AS empleado_id,
                            empleado.email AS empleado_email,
                            empleado.nombre AS empleado_nombre,
                            empleado.apellido AS empleado_apellido,
                            creador.id AS creador_id,
                            creador.email AS creador_email,
                            creador.nombre AS creador_nombre,
                            creador.apellido AS creador_apellido,
                            t.fecha_creacion,
                            t.fecha_limite,
                            t.evidencia,
                            t.estado
                        FROM tarea t
                        LEFT JOIN usuario empleado
                            ON empleado.id = t.empleado_id
                        LEFT JOIN usuario creador
                            ON creador.id = t.creador_id
                        WHERE t.empleado_id = %s
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
                    query = "SELECT * FROM `tarea` WHERE `id` = %s"
                    cursor.execute(query, (id,))
                    tareas = cursor.fetchone()
                    return tareas
        except Exception as e:
            raise e

    def get_by_titulo(self, titulo: str):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM `tarea` WHERE `titulo` = %s"
                    cursor.execute(query, (titulo,))
                    tareas = cursor.fetchone()
                    return tareas
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

    def update_by_id(self, id: int, tarea: CreateTareaSchema):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """UPDATE `tarea` 
                        SET
                            `titulo` = %s,
                            `prioridad` = %s,
                            `tipo` = %s,
                            `empleado_id` = %s,
                            `creador_id` = %s,
                            `fecha_limite` = %s,
                            `evidencia` = %s
                        WHERE `id` = %s"""
                    cursor.execute(
                        query,
                        (
                            tarea.titulo,
                            tarea.prioridad,
                            tarea.tipo,
                            tarea.empleado_id,
                            tarea.creador_id,
                            tarea.fecha_limite,
                            tarea.evidencia,
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
