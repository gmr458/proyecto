from datetime import datetime
from mimesis import Person, Text, Generic, Numeric, Datetime
from mimesis.locales import Locale
from dataclasses import dataclass
from app.config.database import get_mysql_connection

from app.config.jwt import hash_password

id = 2

text = Text(Locale.ES_MX)
generic = Generic()
numeric = Numeric()
mimesis_datetime = Datetime()


@dataclass(frozen=True)
class Task:
    titulo: str
    prioridad: str
    tipo_id: int
    empleado_id: int
    creador_id: int
    fecha_limite: datetime
    estado: str


@dataclass(frozen=True)
class User:
    id: int
    nombre: str
    apellido: str
    email: str
    contrasena: str
    numero_documento: str
    code_country: str
    phone_number: str
    rol_id: int
    activado: bool


admins: list[User] = []

for i in range(4):
    person = Person(Locale.ES_MX)
    admin = User(
        id=id,
        nombre=person.first_name(),
        apellido=person.last_name(),
        code_country="57",
        phone_number=person.phone_number("##########"),
        email=person.email(),
        contrasena=hash_password("password123"),
        numero_documento=person.identifier("##########"),
        rol_id=1,
        activado=True,
    )
    admins.append(admin)
    id = id + 1

print(f"{datetime.now()} - admins generated")

employees: list[User] = []

for i in range(25):
    person = Person(Locale.ES_MX)
    admin = User(
        id=id,
        nombre=person.first_name(),
        apellido=person.last_name(),
        code_country="57",
        phone_number=person.phone_number("##########"),
        email=person.email(),
        contrasena=hash_password("password123"),
        numero_documento=person.identifier("##########"),
        rol_id=2,
        activado=True,
    )
    admins.append(admin)
    id = id + 1

print(f"{datetime.now()} - employees generated")

tasks: list[Task] = []

for i in range(348):
    task = Task(
        titulo=text.sentence(),
        prioridad=generic.random.choice(["baja", "media", "alta"]),
        tipo_id=generic.random.choice([1, 2, 3, 4]),
        empleado_id=numeric.integer_number(start=6, end=30),
        creador_id=numeric.integer_number(start=1, end=5),
        fecha_limite=mimesis_datetime.datetime(start=2023, end=2024),
        estado=generic.random.choice(["sin_iniciar", "en_proceso", "ejecutada"]),
    )
    tasks.append(task)

print(f"{datetime.now()} - tasks generated")


def create_users(users: list[User]):
    connection = get_mysql_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                for user in users:
                    cursor.execute(
                        """
                        INSERT INTO usuario (
                            id,
                            nombre,
                            apellido,
                            email,
                            contrasena,
                            numero_documento,
                            code_country,
                            phone_number,
                            activado
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            user.id,
                            user.nombre,
                            user.apellido,
                            user.email,
                            user.contrasena,
                            user.numero_documento,
                            user.code_country,
                            user.phone_number,
                            True,
                        ),
                    )

                    user_id = cursor.lastrowid

                    cursor.execute(
                        """INSERT INTO `roles_usuario` (
                            `usuario_id`,
                            `rol_id`
                        ) VALUES (%s, %s)""",
                        (
                            user_id,
                            user.rol_id,
                        ),
                    )
            connection.commit()
    except Exception as e:
        raise e


create_users(admins)
print(f"{datetime.now()} - admins inserted in the database")

create_users(employees)
print(f"{datetime.now()} - employees inserted in the database")


def create_tasks(tasks: list[Task]):
    connection = get_mysql_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                for task in tasks:
                    query = """INSERT INTO `tarea` (
                        `titulo`,
                        `prioridad`,
                        `tipo_id`,
                        `empleado_id`,
                        `creador_id`,
                        `fecha_limite`,
                        `evidencia`,
                        `estado`
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(
                        query,
                        (
                            task.titulo,
                            task.prioridad,
                            task.tipo_id,
                            task.empleado_id,
                            task.creador_id,
                            task.fecha_limite,
                            "",
                            task.estado,
                        ),
                    )
            connection.commit()
    except Exception as e:
        raise e


create_tasks(tasks)
print(f"{datetime.now()} - tasks inserted in the database")
