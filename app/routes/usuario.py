from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.config.jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.controllers.usuario import UsuarioController
from app.models.usuario import (
    CreateUsuarioSchema,
    LoginUsuarioSchema,
    ResponseUsuarioSchema,
)

router = APIRouter()
usuario_controller = UsuarioController()


@router.post(
    "/register",
    response_model=ResponseUsuarioSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_usuario(payload: CreateUsuarioSchema):
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

    payload.contrasena = hash_password(str(payload.contrasena))
    payload.email = payload.email.lower()

    usuario_controller.create(payload)
    user_created = usuario_controller.get_by_email(payload.email)
    if user_created is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error obteniendo usuario creado",
        )

    del user_created["contrasena"]
    return user_created


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
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

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=ResponseUsuarioSchema, status_code=status.HTTP_200_OK)
def me(current_user: Annotated[ResponseUsuarioSchema, Depends(get_current_user)]):
    return current_user
