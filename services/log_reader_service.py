from database.db import SessionLocal
from database.models import Circularizacion
import pytz

zona = pytz.timezone("Europe/Madrid")


def leer_historial():

    db = SessionLocal()

    try:

        registros = db.query(Circularizacion).all()

        resultado = []

        for r in registros:

            # 🔥 CONVERSIÓN A HORA LOCAL (ESPAÑA)
            fecha_local = r.fecha.astimezone(zona)

            resultado.append({
                "fecha": fecha_local.strftime("%Y-%m-%d %H:%M:%S"),
                "excel": r.excel,
                "correo": r.correo,
                "destinatarios": r.destinatarios
            })

        return resultado

    finally:

        db.close()