import datetime
import os

# carpeta de logs compatible con Vercel
LOG_FOLDER = "/tmp/logs"
LOG_FILE = f"{LOG_FOLDER}/circularizaciones.log"

# crear carpeta si no existe
os.makedirs(LOG_FOLDER, exist_ok=True)


def registrar_circularizacion(nombre_excel, total_destinatarios, correo_remitente):

    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    registro = f"""
=====================================
Fecha: {fecha}
Excel: {nombre_excel}
Correo: {correo_remitente}
Destinatarios: {total_destinatarios}
Estado: iniciada
=====================================
"""

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(registro)