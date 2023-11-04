from enum import Enum


class Estado(str, Enum):
    sin_iniciar = "sin_iniciar"
    en_proceso = "en_proceso"
    ejecutada = "ejecutada"
