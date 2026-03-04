import datetime

LOG_FILE = "logs/circularizaciones.log"


def registrar_circularizacion(nombre_excel, total_destinatarios):

    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    registro = f"""
=====================================
Fecha: {fecha}
Excel: {nombre_excel}
Destinatarios: {total_destinatarios}
Estado: iniciada
=====================================
"""

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(registro)