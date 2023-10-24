from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.config.jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.controllers.rol import RolController
from app.controllers.usuario import UsuarioController
from app.models.rol import NombreRol
from app.models.usuario import (
    CreateUsuarioSchema,
    LoginUsuarioSchema,
    ResponseUsuarioSchema,
)

router = APIRouter()

usuario_controller = UsuarioController()
rol_controller = RolController()


@router.post(
    "/",
    response_model=ResponseUsuarioSchema,
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
            detail="No tiene permisos para hacer esta operación",
        )

    user_found = usuario_controller.get_by_email(payload.email.lower())
    if user_found is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con este email",
        )

    user_found = usuario_controller.get_by_numero_documento(payload.numero_documento)
    if user_found is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con este número de documento",
        )

    user_found = usuario_controller.get_by_telefono(payload.telefono)
    if user_found is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con este número de telefono",
        )

    role_found = rol_controller.get_by_id(payload.rol_id)
    if role_found is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rol enviado no existe",
        )

    payload.contrasena = hash_password(str(payload.contrasena))
    payload.email = payload.email.lower()

    usuario_controller.create(payload)
    user_created = usuario_controller.get_by_email(payload.email)
    if user_created is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error obteniendo usuario creado",
        )

    rol_controller.create_para_usuario(payload.rol_id, user_created["id"])

    del user_created["contrasena"]
    return user_created


@router.post("/login", status_code=status.HTTP_200_OK)
def login(payload: LoginUsuarioSchema):
    user = usuario_controller.get_by_email(payload.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No existe un usuario con este email",
        )

    if not verify_password(payload.contrasena, user["contrasena"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta",
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


@router.get(
    "/perfil", response_model=ResponseUsuarioSchema, status_code=status.HTTP_200_OK
)
def mi_perfil(
    current_user: Annotated[ResponseUsuarioSchema, Depends(get_current_user)]
):
    return current_user
