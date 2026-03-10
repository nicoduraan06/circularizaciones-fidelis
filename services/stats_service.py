from database.db import SessionLocal
from database.models import Circularizacion


def obtener_estadisticas():

    db = SessionLocal()

    try:

        registros = db.query(Circularizacion).all()

        total_circularizaciones = len(registros)

        total_destinatarios = sum(
            r.destinatarios for r in registros
        )

        ultimos = []

        for r in registros[-5:][::-1]:

            ultimos.append({
                "fecha": r.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "excel": r.excel,
                "remitente": r.correo,
                "destinatarios": r.destinatarios
            })

        return {
            "total_circularizaciones": total_circularizaciones,
            "total_destinatarios": total_destinatarios,
            "ultimos": ultimos
        }

    finally:

        db.close()