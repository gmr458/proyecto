import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import observacion, tareas, usuario
from app.startup import crear_usuario_admin

app = FastAPI()

load_dotenv()

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

CORS_ALLOW_ORIGINS = os.environ.get("CORS_ALLOW_ORIGINS")
if CORS_ALLOW_ORIGINS is not None and CORS_ALLOW_ORIGINS != "":
    for origin in CORS_ALLOW_ORIGINS.split(","):
        origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    usuario.router,
    tags=["Usuarios"],
    prefix="/api/usuarios",
)
app.include_router(
    tareas.router,
    tags=["Tareas"],
    prefix="/api/tareas",
)
app.include_router(
    observacion.router,
    tags=["Observaciones"],
    prefix="/api/observaciones",
)

crear_usuario_admin()
