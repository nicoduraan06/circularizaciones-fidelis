estado_envio = {
    "total": 0,
    "enviados": 0
}


def iniciar_progreso(total):

    estado_envio["total"] = total
    estado_envio["enviados"] = 0


def incrementar_enviados():

    estado_envio["enviados"] += 1


def obtener_progreso():

    return estado_envio