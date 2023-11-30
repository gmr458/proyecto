from app.config.database import get_mysql_connection
from app.models.observacion_base_schema import ObservacionBaseSchema


class ObservacionController:
    def create(self, observacion: ObservacionBaseSchema, tarea_id: int):
        connection = get_mysql_connection()
        inserted_id = None

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO observacion (
                            tarea_id,
                            creador_id,
                            contenido
                        ) VALUES (%s, %s, %s)
                        """,
                        (
                            tarea_id,
                            observacion.creador_id,
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
                    query = """
                        SELECT
                            observacion.id,
                            observacion.tarea_id,
                            observacion.creador_id,
                            usuario.nombre AS creador_nombre,
                            usuario.apellido AS creador_apellido,
                            usuario.email AS creador_email,
                            observacion.contenido,
                            observacion.fecha_creacion
                        FROM observacion
                        JOIN usuario ON
                            usuario.id = observacion.creador_id
                        WHERE observacion.eliminado = false
                            AND observacion.id = %s
                    """
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
                    query = """
                        SELECT
                            observacion.id,
                            observacion.tarea_id,
                            observacion.creador_id,
                            usuario.nombre AS creador_nombre,
                            usuario.apellido AS creador_apellido,
                            usuario.email AS creador_email,
                            observacion.contenido,
                            observacion.fecha_creacion
                        FROM observacion
                        JOIN usuario ON
                            usuario.id = observacion.creador_id
                        WHERE observacion.eliminado = false
                            AND observacion.tarea_id = %s
                    """
                    cursor.execute(query, (tarea_id,))
                    tareas = cursor.fetchall()
                    return tareas
        except Exception as e:
            raise e

    def get_by_creador_id(self, creador_id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT
                            observacion.id,
                            observacion.tarea_id,
                            observacion.creador_id,
                            usuario.nombre AS creador_nombre,
                            usuario.apellido AS creador_apellido,
                            usuario.email AS creador_email,
                            observacion.contenido,
                            observacion.fecha_creacion
                        FROM observacion
                        JOIN usuario ON
                            usuario.id = observacion.creador_id
                        WHERE observacion.eliminado = false
                            AND observacion.creador_id = %s
                    """
                    cursor.execute(query, (creador_id,))
                    tareas = cursor.fetchall()
                    return tareas
        except Exception as e:
            raise e

    def delete_by_id(self, id: int):
        connection = get_mysql_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    query = """
                        UPDATE observacion
                        SET eliminado = true
                        WHERE id = %s
                    """
                    cursor.execute(query, (id,))
                connection.commit()
        except Exception as e:
            raise e
