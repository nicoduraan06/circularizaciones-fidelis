import csv
import os
from app.mailer import enviar_correo

ERROR_LOG = "logs/errores_envio.csv"


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

        # eliminar error del CSV
        if os.path.exists(ERROR_LOG):

            registros = []

            with open(ERROR_LOG, newline="", encoding="utf-8") as f:

                reader = csv.DictReader(f)

                for row in reader:

                    if row["destinatario"] != destinatario:
                        registros.append(row)

            with open(ERROR_LOG, "w", newline="", encoding="utf-8") as f:

                writer = csv.DictWriter(f, fieldnames=["fecha","destinatario","error"])

                writer.writeheader()

                writer.writerows(registros)

        return True

    except Exception as e:

        print(f"Error al reintentar envío a {destinatario}: {e}")

        return False