from datetime import datetime
import csv
import os

LOG_FILE = "logs/errores_envio.csv"


def registrar_error(destinatario, error):

    os.makedirs("logs", exist_ok=True)

    existe = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        if not existe:
            writer.writerow(["fecha", "destinatario", "error"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            destinatario,
            str(error)
        ])