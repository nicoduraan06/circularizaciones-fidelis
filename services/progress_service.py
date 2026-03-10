import json
import os

# archivo temporal para guardar progreso
PROGRESS_FILE = "/tmp/progreso_envio.json"


def iniciar_progreso(total):

    estado_envio = {
        "total": total,
        "enviados": 0,
        "errores": 0
    }

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(estado_envio, f)


def incrementar_enviados():

    estado = obtener_progreso()
    estado["enviados"] += 1

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f)


def incrementar_errores():

    estado = obtener_progreso()
    estado["errores"] += 1

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f)


def obtener_progreso():

    if not os.path.exists(PROGRESS_FILE):
        return {
            "total": 0,
            "enviados": 0,
            "errores": 0
        }

    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)