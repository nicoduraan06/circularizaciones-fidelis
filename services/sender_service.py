import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.mailer import enviar_correo
from services.progress_service import iniciar_progreso, incrementar_enviados, incrementar_errores
from services.error_logger_service import registrar_error

UPLOAD_FOLDER = "uploads"


def enviar_un_correo(
        d,
        email_remitente,
        password,
        asunto,
        mensaje
):

    email_destino = d["email"]
    documentos = d["documentos"]

    archivos_adjuntos = []

    # evitar PDFs duplicados
    documentos_unicos = list(set(documentos))

    for doc in documentos_unicos:

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

        return {"email": email_destino, "error": None}

    except Exception as e:

        print(f"❌ Error enviando a {email_destino}: {e}")

        registrar_error(email_destino, e)

        return {"email": email_destino, "error": str(e)}


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

    # ⚠ Reducimos paralelismo para evitar bloqueos SMTP
    max_workers = 2

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        futures = [
            executor.submit(
                enviar_un_correo,
                d,
                email_remitente,
                password,
                asunto,
                mensaje
            )
            for d in destinatarios
        ]

        for future in as_completed(futures):

            resultado = future.result()

            if resultado["error"]:

                errores.append(resultado["email"])
                incrementar_errores()

            incrementar_enviados()

    print("===== FIN DE LA CIRCULARIZACIÓN =====")

    # enviar resumen al remitente
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