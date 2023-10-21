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
                    ) VALUES (%s, %s, %s, %s, %s)"""
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
                    query = "SELECT * FROM `tarea`"
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
                    query = "SELECT * FROM `tarea` WHERE `usuario_id` = %s"
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
