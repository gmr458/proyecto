from enum import Enum


class Tipo(str, Enum):
    quimico = "quimico"
    agua = "agua"
    aire = "aire"
    reciclaje = "reciclaje"
