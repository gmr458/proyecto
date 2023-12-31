from typing import Annotated, Any

from fastapi import Depends, HTTPException, status

from app.config.jwt import get_current_user
from app.controllers.observacion import ObservacionController
from app.controllers.rol import RolController
from app.controllers.tarea import TareaController
from app.controllers.usuario import UsuarioController
from app.util.api_router import APIRouter
from app.models.observacion_base_schema import ObservacionBaseSchema
from app.models.rol import NombreRol

router = APIRouter()

usuario_controller = UsuarioController()
tarea_controller = TareaController()
rol_controller = RolController()
observacion_controller = ObservacionController()


@router.post("/tarea/{tarea_id}", status_code=status.HTTP_201_CREATED)
def create_observacion(
    tarea_id: int,
    payload: ObservacionBaseSchema,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False
    es_empleado = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True
            break

        if rol["nombre"] == NombreRol.empleado:
            es_empleado = True
            break

    if es_admin is False and es_empleado is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "No tiene permisos para hacer esta operación",
                "cause": "bad_auth",
            },
        )

    tarea_found = tarea_controller.get_by_id(tarea_id)
    if tarea_found is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "No puede crear observaciones para una tarea que no existe",
                "cause": "tarea_id",
            },
        )

    if es_empleado and current_user["id"] != tarea_found["empleado_id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "No tiene permisos para hacer esta operación",
                "cause": "bad_auth",
            },
        )

    payload.creador_id = current_user["id"]
    inserted_id = observacion_controller.create(payload, tarea_id)
    observacion_creada = observacion_controller.get_by_id(inserted_id)
    if observacion_creada is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error obteniendo observacion creada",
        )

    return {"msg": "Observación creada", "observacion": observacion_creada}


@router.get("/tarea/{tarea_id}", status_code=status.HTTP_200_OK)
def obtener_observaciones_de_una_tarea(
    tarea_id: int,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_empleado = False
    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.empleado:
            es_empleado = True

        if rol["nombre"] == NombreRol.administrador:
            es_admin = True

    if es_empleado is False and es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    tarea_found = tarea_controller.get_by_id(tarea_id)
    if tarea_found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe esa tarea y por lo tanto tampoco observaciones",
        )

    if es_empleado and current_user["id"] != tarea_found["empleado_id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    observaciones = observacion_controller.get_by_tarea_id(tarea_id)

    return {"observaciones": observaciones, "tarea_id": tarea_id}


@router.get(
    "/{observacion_id}",
    status_code=status.HTTP_200_OK,
)
def obtener_una_observacion(
    observacion_id: int,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_empleado = False
    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.empleado:
            es_empleado = True

        if rol["nombre"] == NombreRol.administrador:
            es_admin = True

    if es_empleado is False and es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    observacion = observacion_controller.get_by_id(observacion_id)
    if observacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observación no encontrada",
        )

    tarea = tarea_controller.get_by_id(observacion["tarea_id"])
    if tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tara a la que pertenece la observación no encontrada",
        )

    if es_empleado and current_user["id"] != tarea["empleado_id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    return {"observacion": observacion}


@router.delete(
    "/{observacion_id}",
    status_code=status.HTTP_200_OK,
)
def delete_observacion(
    observacion_id: int,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_empleado = False
    es_admin = False

    for rol in roles:
        if rol["nombre"] == NombreRol.empleado:
            es_empleado = True

        if rol["nombre"] == NombreRol.administrador:
            es_admin = True

    if es_empleado is False and es_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    observacion = observacion_controller.get_by_id(observacion_id)

    if observacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observación no encontrada",
        )

    if es_empleado and current_user["id"] != observacion["creador_id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    observacion_controller.delete_by_id(observacion_id)

    return {"mensaje": "Observación eliminada"}
