from database.db import SessionLocal
from database.models import Circularizacion


def leer_historial():

    db = SessionLocal()

    try:

        registros = db.query(Circularizacion).all()

        resultado = []

        for r in registros:

            resultado.append({
                "fecha": r.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "excel": r.excel,
                "correo": r.correo,
                "destinatarios": r.destinatarios
            })

        return resultado

    finally:

        db.close()