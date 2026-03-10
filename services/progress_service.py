from database.db import SessionLocal
from database.models import Circularizacion

estado_envio = {
    "total": 0,
    "enviados": 0,
    "errores": 0
}


def iniciar_progreso(total):

    estado_envio["total"] = total
    estado_envio["enviados"] = 0
    estado_envio["errores"] = 0


def incrementar_enviados():
    estado_envio["enviados"] += 1


def incrementar_errores():
    estado_envio["errores"] += 1


def obtener_progreso():
    return estado_envio