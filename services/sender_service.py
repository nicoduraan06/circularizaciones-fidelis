from app.mailer import enviar_correo
import os

UPLOAD_FOLDER = "uploads"

def procesar_circularizacion(destinatarios, email_remitente, password, asunto, mensaje):

    print("===== INICIO ENVÍO DE CIRCULARIZACIÓN =====")

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

        except Exception as e:
            print(f"❌ Error enviando a {email_destino}: {e}")

    print("===== FIN DE LA CIRCULARIZACIÓN =====")