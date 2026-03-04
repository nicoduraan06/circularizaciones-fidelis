import csv
import os
from app.mailer import enviar_correo

ERROR_LOG = "logs/errores_envio.csv"
UPLOAD_FOLDER = "uploads"


def reintentar_error(email_remitente, password, destinatario, asunto, mensaje):

    try:

        enviar_correo(
            email_remitente,
            password,
            destinatario,
            asunto,
            mensaje,
            []
        )

        return True

    except Exception as e:

        print(f"Error al reintentar envío a {destinatario}: {e}")

        return False