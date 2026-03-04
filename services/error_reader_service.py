import csv
import os

LOG_FILE = "logs/errores_envio.csv"


def leer_errores():

    if not os.path.exists(LOG_FILE):
        return []

    registros = []

    with open(LOG_FILE, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:
            registros.append(row)

    return registros