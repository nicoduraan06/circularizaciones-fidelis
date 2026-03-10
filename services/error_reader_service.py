import csv
import os

# carpeta temporal compatible con Vercel
LOG_DIR = "/tmp/logs"
LOG_FILE = os.path.join(LOG_DIR, "errores_envio.csv")


def leer_errores():

    if not os.path.exists(LOG_FILE):
        return []

    registros = []

    with open(LOG_FILE, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:
            registros.append(row)

    # ordenar por fecha descendente
    registros.sort(key=lambda x: x["fecha"], reverse=True)

    return registros