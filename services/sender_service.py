import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.mailer import enviar_correo
from services.progress_service import iniciar_progreso, incrementar_enviados, incrementar_errores
from services.error_logger_service import registrar_error

# carpeta temporal compatible con Vercel
UPLOAD_FOLDER = "/tmp/uploads"


def enviar_un_correo(
        d,
        email_remitente,
        password,
        asunto,
        mensaje,
        cc
):

    email_destino = d["email"]
    documentos = d["documentos"]

    archivos_adjuntos = []

    # asegurarnos de que documentos sea lista
    if isinstance(documentos, str):
        documentos = [doc.strip() for doc in documentos.split(",") if doc.strip()]

    # evitar PDFs duplicados
    documentos_unicos = list(set(documentos))

    for doc in documentos_unicos:

        ruta_pdf = os.path.join(UPLOAD_FOLDER, doc)

        if os.path.exists(ruta_pdf):
            archivos_adjuntos.append(ruta_pdf)
        else:
            print(f"⚠ PDF no encontrado: {ruta_pdf}")

    try:

        print(f"📧 Enviando correo a: {email_destino}")
        print(f"📎 Adjuntos: {archivos_adjuntos}")

        enviar_correo(
            email_remitente,
            password,
            email_destino,
            asunto,
            mensaje,
            archivos_adjuntos,
            cc
        )

        print(f"✅ Correo enviado correctamente a {email_destino}")

        return {"email": email_destino, "error": None}

    except Exception as e:

        print(f"❌ Error enviando a {email_destino}: {e}")

        registrar_error(email_destino, str(e))

        return {"email": email_destino, "error": str(e)}


def procesar_circularizacion(
        destinatarios,
        email_remitente,
        password,
        asunto,
        mensaje,
        cc
):

    print("===== INICIO ENVÍO DE CIRCULARIZACIÓN =====")

    total = len(destinatarios)

    # iniciar progreso
    iniciar_progreso(total)

    errores = []

    # paralelismo controlado para SMTP
    max_workers = 2

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        futures = [
            executor.submit(
                enviar_un_correo,
                d,
                email_remitente,
                password,
                asunto,
                mensaje,
                cc
            )
            for d in destinatarios
        ]

        for future in as_completed(futures):

            try:

                resultado = future.result()

                if resultado["error"]:

                    errores.append(resultado["email"])
                    incrementar_errores()

                incrementar_enviados()

            except Exception as e:

                print("❌ Error inesperado en worker:", e)

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
                [],
                cc
            )

        except Exception as e:

            print("❌ Error enviando email resumen:", e)