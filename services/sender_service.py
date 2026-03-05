import os
import time
from app.mailer import enviar_correo
from services.progress_service import iniciar_progreso, incrementar_enviados, incrementar_errores
from services.error_logger_service import registrar_error

UPLOAD_FOLDER = "uploads"


def procesar_circularizacion(
        destinatarios,
        email_remitente,
        password,
        asunto,
        mensaje
):

    print("===== INICIO ENVÍO DE CIRCULARIZACIÓN =====")

    total = len(destinatarios)

    iniciar_progreso(total)

    errores = []

    for d in destinatarios:

        email_destino = d["email"]
        documentos = d["documentos"]

        archivos_adjuntos = []

        for doc in documentos:

            ruta_pdf = os.path.join(UPLOAD_FOLDER, doc)

            if os.path.exists(ruta_pdf):
                archivos_adjuntos.append(ruta_pdf)
            else:
                print(f"⚠ PDF no encontrado: {ruta_pdf}")

        try:

            print(f"Enviando correo a: {email_destino}")
            print(f"Adjuntos: {archivos_adjuntos}")

            enviar_correo(
                email_remitente,
                password,
                email_destino,
                asunto,
                mensaje,
                archivos_adjuntos
            )

            print(f"Correo enviado correctamente a {email_destino}")

            incrementar_enviados()

        except Exception as e:

            print(f"❌ Error enviando a {email_destino}: {e}")

            registrar_error(email_destino, e)

            errores.append(email_destino)

            incrementar_errores()

            incrementar_enviados()

        time.sleep(1)

    print("===== FIN DE LA CIRCULARIZACIÓN =====")

    # 🔹 enviar resumen al remitente
    if errores:

        asunto_resumen = "Resultado de circularización"

        mensaje_resumen = f"""
La circularización ha finalizado.

Correos enviados: {total - len(errores)}
Errores detectados: {len(errores)}

No se pudieron enviar los siguientes correos:

{chr(10).join(errores)}
"""

        try:

            enviar_correo(
                email_remitente,
                password,
                email_remitente,
                asunto_resumen,
                mensaje_resumen,
                []
            )

        except Exception as e:

            print("Error enviando email resumen:", e)