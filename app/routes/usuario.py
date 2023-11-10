from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
import pandas as pd
from phonenumbers import (
    NumberParseException,
    is_valid_number,
    parse as parse_phone_number,
)
import pymysql
from pymysql.err import IntegrityError

from app.config.jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.controllers.rol import RolController
from app.controllers.usuario import UsuarioController
from app.models.rol import NombreRol
from app.models.create_usuario_schema import CreateUsuarioSchema
from app.models.login_usuario_schema import LoginUsuarioSchema

router = APIRouter()

usuario_controller = UsuarioController()
rol_controller = RolController()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_usuario(
    payload: CreateUsuarioSchema,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

    if es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "No tiene permisos para hacer esta operación",
                "cause": "bad_auth",
            },
        )

    try:
        parsed_phone_number = parse_phone_number(
            f"+{payload.code_country}{payload.phone_number}",
            None,
        )
        is_valid = is_valid_number(parsed_phone_number)
        if is_valid is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"msg": "Número de telefono invalido", "cause": "number"},
            )
    except NumberParseException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "Número de telefono invalido", "cause": "number"},
        )

    user_found = usuario_controller.get_by_telefono(payload.phone_number)
    if user_found is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "msg": "Ya existe un usuario con este número de telefono",
                "cause": "number",
            },
        )

    user_found = usuario_controller.get_by_email(payload.email.lower())
    if user_found is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"msg": "Ya existe un usuario con este email", "cause": "email"},
        )

    user_found = usuario_controller.get_by_numero_documento(payload.numero_documento)
    if user_found is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "msg": "Ya existe un usuario con este número de documento",
                "cause": "numero_documento",
            },
        )

    role_found = rol_controller.get_by_id(payload.rol_id)
    if role_found is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "El rol enviado no existe", "cause": "rol_id"},
        )

    payload.contrasena = hash_password(str(payload.contrasena))
    payload.email = payload.email.lower()

    try:
        usuario_controller.create(payload)
    except pymysql.err.IntegrityError as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "msg": "El email, numero de documento o numero de telefono ya estan siendo usados"
            },
        )

    user_created = usuario_controller.get_by_email(payload.email)
    if user_created is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"msg": "Error obteniendo usuario creado", "cause": "internal"},
        )

    del user_created["contrasena"]

    return {"msg": "Usuario creado", "data": {"user": user_created}}


@router.post("/upload/")
async def upload_file(
    file: UploadFile,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

    if es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "No tiene permisos para hacer esta operación",
                "cause": "bad_auth",
            },
        )

    if file.content_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "El tipo de contenido del archivo enviado es desconocido",
                "cause": "file",
            },
        )

    content_type = file.content_type

    if (
        content_type
        != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        and content_type != "application/vnd.ms-excel"
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "El archivo debe ser de Excel",
                "cause": "file",
            },
        )

    dataframe = pd.read_excel(file.file.read())

    validate_fields = [
        "nombre",
        "apellido",
        "code_country",
        "phone_number",
        "email",
        "contrasena",
        "numero_documento",
        "rol_id",
    ]
    for field in validate_fields:
        if field not in dataframe.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": """El archivo Excel no cumple con la estructura requerida,
                        debe tener las columnas nombre, apellido, code_country, phone_number, email,
                        contrasena, numero_documento y rol_id.""",
                    "cause": "file",
                },
            )

    dataframe["code_country"] = dataframe["code_country"].astype(str)
    dataframe["phone_number"] = dataframe["phone_number"].astype(str)
    dataframe["numero_documento"] = dataframe["numero_documento"].astype(str)
    dataframe["rol_id"] = pd.to_numeric(
        dataframe["rol_id"],
        errors="coerce",
        downcast="integer",
    )
    dataframe["contrasena"] = dataframe["contrasena"].apply(hash_password)

    users_list: list[CreateUsuarioSchema] = []
    for _, row in dataframe.iterrows():
        user = CreateUsuarioSchema(
            nombre=str(row["nombre"]),
            apellido=str(row["apellido"]),
            code_country=str(row["code_country"]),
            phone_number=str(row["phone_number"]),
            email=str(row["email"]),
            numero_documento=str(row["numero_documento"]),
            contrasena=str(row["contrasena"]),
            rol_id=int(row["rol_id"]),
        )
        users_list.append(user)

    users_created = []
    users_no_created = []

    for user in users_list:
        try:
            usuario_controller.create(user)
        except IntegrityError:
            users_no_created.append(
                {
                    "reason": "Ya existe",
                    "user": user.model_dump(exclude={"contrasena"}),
                }
            )
            continue

        user_created = usuario_controller.get_by_email(user.email)
        if user_created:
            del user_created["contrasena"]
            users_created.append(user_created)

    if len(users_created) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": """Ningun usuario fue creado.
                    Revisa la integridad de los datos del archivo excel,
                    No se pueden crear usuarios que ya existen.""",
                "cause": "file",
            },
        )

    if len(users_no_created) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": f"""{len(users_created)} Usuario/s creados.
                    {len(users_no_created)} Usuario/s no creados.
                    Algunos usuarios no fueron creados,
                    revisa la integridad de los datos del archivo excel,
                    no se pueden crear usuarios que ya existen.""",
                "cause": "file",
            },
        )

    return {
        "msg": f"{len(users_created)} Usuario/s creados",
        "data": {
            "users_created": users_created,
        },
    }


@router.post("/login", status_code=status.HTTP_200_OK)
def login(payload: LoginUsuarioSchema):
    user = usuario_controller.get_by_email(payload.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "No existe un usuario con este email", "cause": "email"},
        )

    if not verify_password(payload.contrasena, user["contrasena"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Contraseña incorrecta", "cause": "contrasena"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    roles = rol_controller.get_by_user_id(user["id"])

    return {
        "email": user["email"],
        "roles": [r["nombre"] for r in roles],
        "token": access_token,
    }


@router.get("/perfil", status_code=status.HTTP_200_OK)
def mi_perfil(
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
):
    return current_user


@router.get("/all")
def get_all(
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

    if es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    users = usuario_controller.get_all()

    return {"msg": "Todos los usuarios", "data": {"users": users}}


@router.get("/top/tareas/ejecutadas")
def get_top_tareas_ejecutadas(
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

    if es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    users = usuario_controller.get_top_mas_tareas_ejecutadas()

    return {"msg": "Top usuarios con más tareas ejecutadas", "data": {"users": users}}


@router.get("/top/tareas/en_proceso")
def get_top_tareas_en_proceso(
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

    if es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    users = usuario_controller.get_top_mas_tareas_en_proceso()

    return {"msg": "Top usuarios con más tareas en proceso", "data": {"users": users}}


@router.get("/top/tareas/sin_iniciar")
def get_top_tareas_sin_iniciar(
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

    if es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    users = usuario_controller.get_top_mas_tareas_sin_iniciar()

    return {"msg": "Top usuarios con más tareas sin iniciar", "data": {"users": users}}


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def delete_usuario(
    usuario_id: int,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

    if es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    if usuario_id == current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminarte a ti mismo",
        )

    user = usuario_controller.get_by_id(usuario_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    usuario_controller.delete_by_id(usuario_id)

    return {"msg": "Usuario eliminado"}


@router.get("/top/tareas/asignadas")
def get_top_tareas_asignadas(
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

    if es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    users = usuario_controller.get_top_mas_tareas_asignadas()

    return {"msg": "Top usuarios con más tareas asignadas", "data": {"users": users}}
