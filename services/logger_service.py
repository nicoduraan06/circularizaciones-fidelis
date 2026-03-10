from database.db import SessionLocal
from database.models import Circularizacion


def registrar_circularizacion(nombre_excel, total_destinatarios, correo_remitente):

    db = SessionLocal()

    try:

        registro = Circularizacion(
            excel=nombre_excel,
            correo=correo_remitente,
            destinatarios=total_destinatarios
        )

        db.add(registro)
        db.commit()

    finally:

        db.close()