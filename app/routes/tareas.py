from typing import Annotated, Any

from fastapi import Depends, HTTPException, status

from app.config.jwt import get_current_user
from app.controllers.rol import RolController
from app.controllers.tarea import TareaController
from app.controllers.usuario import UsuarioController
from app.util.api_router import APIRouter
from app.models.rol import NombreRol
from app.models.tarea_base_schema import TareaBaseSchema

router = APIRouter()

usuario_controller = UsuarioController()
tarea_controller = TareaController()
rol_controller = RolController()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_tarea(
    payload: TareaBaseSchema,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    print(f"current user {current_user}")
    print(f"payload {payload}")

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

    tareas_found = tarea_controller.get_by_titulo(payload.titulo)
    if tareas_found is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "msg": "Ya existe una tarea con ese titulo",
                "cause": "titulo",
            },
        )

    usuario_found = usuario_controller.get_by_id(payload.empleado_id)
    if usuario_found is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "El usuario al que desea asignar la tarea no existe",
                "cause": "empleado_id",
            },
        )

    roles_usuario = rol_controller.get_by_user_id(usuario_found["id"])

    usuario_es_admin = False

    for rol in roles_usuario:
        if rol["nombre"] == NombreRol.administrador:
            usuario_es_admin = True
            break

    if usuario_es_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "No puede asignar una tarea a un administrador",
                "cause": "empleado_id",
            },
        )

    payload.creador_id = current_user["id"]
    tarea_controller.create(payload)
    tarea_created = tarea_controller.get_by_titulo(payload.titulo)
    if tarea_created is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error obteniendo tarea creada",
        )

    return {"msg": "Tarea creada", "tarea": tarea_created}


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_tareas(current_user: Annotated[dict[str, Any], Depends(get_current_user)]):
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

    tareas = tarea_controller.get_all()

    return {"msg": "Todas las tareas", "data": {"tasks": tareas}}


@router.get(
    "/mis",
    status_code=status.HTTP_200_OK,
)
def get_mis_tareas(
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_empleado = False

    for rol in roles:
        if rol["nombre"] == NombreRol.empleado:
            es_empleado = True
            break

    if es_empleado is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    tareas = tarea_controller.get_by_usuario_id(current_user["id"])

    return {"msg": "Todas las tareas", "data": {"tasks": tareas}}


@router.get(
    "/{tarea_id}",
    status_code=status.HTTP_200_OK,
)
def get_one_tarea(
    tarea_id: int,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    roles = rol_controller.get_by_user_id(current_user["id"])

    es_admin = False
    es_empleado = False

    for rol in roles:
        if rol["nombre"] == NombreRol.administrador:
            es_admin = True

        if rol["nombre"] == NombreRol.empleado:
            es_empleado = True

    if es_admin is False and es_empleado is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    tarea = tarea_controller.get_by_id(tarea_id)

    if tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )

    if es_empleado and current_user["id"] != tarea["empleado_id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para hacer esta operación",
        )

    return {"tarea": tarea}


@router.get(
    "/empleado/{empleado_id}",
    status_code=status.HTTP_200_OK,
)
def get_all_tareas_by_empleado_id(
    empleado_id: int,
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

    usuario_found = usuario_controller.get_by_id(empleado_id)
    if usuario_found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario al que desea consultar tareas no existe",
        )

    roles_usuario = rol_controller.get_by_user_id(usuario_found["id"])

    usuario_es_admin = False

    for rol in roles_usuario:
        if rol["nombre"] == NombreRol.administrador:
            usuario_es_admin = True
            break

    if usuario_es_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un administrador no tiene tareas asignadas",
        )

    tareas = tarea_controller.get_by_usuario_id(empleado_id)

    return {"tareas": tareas}


@router.get("/count/all")
def get_count_all(current_user: Annotated[dict[str, Any], Depends(get_current_user)]):
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

    total_tasks = tarea_controller.get_count_all()

    return {"msg": "Total tareas", "data": {"total_tasks": total_tasks}}


@router.get("/count/sin_iniciar")
def get_count_sin_iniciar(
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

    tareas_sin_iniciar = tarea_controller.get_count_sin_iniciar()

    return {
        "msg": "Total tareas sin iniciar",
        "data": {"tareas_sin_iniciar": tareas_sin_iniciar},
    }


@router.get("/count/en_proceso")
def get_count_en_proceso(
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

    tareas_en_proceso = tarea_controller.get_count_en_proceso()

    return {
        "msg": "Total tareas en proceso",
        "data": {"tareas_en_proceso": tareas_en_proceso},
    }


@router.get("/count/ejecutadas")
def get_count_ejecutadas(
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

    tareas_ejecutadas = tarea_controller.get_count_ejecutadas()

    return {
        "msg": "Total tareas ejecutadas",
        "data": {"tareas_ejecutadas": tareas_ejecutadas},
    }


@router.put(
    "/{tarea_id}",
    status_code=status.HTTP_200_OK,
)
def update_tarea(
    tarea_id: int,
    payload: TareaBaseSchema,
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

    tarea = tarea_controller.get_by_id(tarea_id)
    if tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )

    if tarea["titulo"] != payload.titulo:
        tarea_found = tarea_controller.get_by_titulo(payload.titulo)
        if tarea_found is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El titulo ya esta siendo usado por otra tarea",
            )

    usuario_found = usuario_controller.get_by_id(payload.empleado_id)
    if usuario_found is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario al que desea asignar la tarea no existe",
        )

    tarea_controller.update_by_id(tarea_id, payload)
    tarea_actualizada = tarea_controller.get_by_id(tarea_id)
    if tarea_actualizada is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error obteniendo tarea actualizada",
        )

    return {"mensaje": "Tarea actualizada", "tarea_actualizada": tarea_actualizada}


@router.delete(
    "/{tarea_id}",
    status_code=status.HTTP_200_OK,
)
def delete_tarea(
    tarea_id: int,
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

    tarea = tarea_controller.get_by_id(tarea_id)

    if tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "msg": "Tarea no encontrada",
                "cause": "id",
            },
        )

    tarea_controller.delete_by_id(tarea_id)

    return {"msg": "Tarea eliminada"}
