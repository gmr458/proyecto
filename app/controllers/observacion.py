from app.config.database import get_mysql_connection
from app.models.observacion import CreateObservacionSchema


class ObservacionController:
    def create(self, observacion: CreateObservacionSchema, tarea_id: int):
        connection = get_mysql_connection()
        inserted_id = None

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """INSERT INTO `observacion` (
                        `tarea_id`,
                        `contenido`
                    ) VALUES (%s, %s)"""
                    cursor.execute(
                        query,
                        (
                            tarea_id,
                            observacion.contenido,
                        ),
                    )
                    inserted_id = cursor.lastrowid
                connection.commit()
                return inserted_id
        except Exception as e:
            raise e

    def get_by_id(self, id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM `observacion` WHERE `id` = %s"
                    cursor.execute(query, (id,))
                    tareas = cursor.fetchone()
                    return tareas
        except Exception as e:
            raise e

    def get_by_tarea_id(self, tarea_id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM `observacion` WHERE `tarea_id` = %s"
                    cursor.execute(query, (tarea_id,))
                    tareas = cursor.fetchall()
                    return tareas
        except Exception as e:
            raise e

    def delete_by_id(self, id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = "DELETE FROM `observacion` WHERE `id` = %s"
                    cursor.execute(query, (id,))
                connection.commit()
        except Exception as e:
            raise e
