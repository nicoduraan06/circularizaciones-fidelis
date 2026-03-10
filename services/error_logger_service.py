from datetime import datetime
import csv
import os

# carpeta temporal compatible con Vercel
LOG_DIR = "/tmp/logs"
LOG_FILE = os.path.join(LOG_DIR, "errores_envio.csv")


def registrar_error(destinatario, error):

    os.makedirs(LOG_DIR, exist_ok=True)

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