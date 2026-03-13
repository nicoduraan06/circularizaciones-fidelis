import smtplib
from email.message import EmailMessage
import os
import requests


def enviar_correo(remitente, password, destinatario, asunto, mensaje, archivos, cc=None):

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente

    # permitir múltiples destinatarios separados por coma
    if isinstance(destinatario, str):
        destinatarios = [d.strip() for d in destinatario.split(",") if d.strip()]
    else:
        destinatarios = destinatario

    msg["To"] = ", ".join(destinatarios)

    # procesar CC
    cc_limpio = []
    if cc:
        if isinstance(cc, str):
            cc_limpio = [c.strip() for c in cc.split(",") if c.strip()]
        else:
            cc_limpio = cc
        msg["Cc"] = ", ".join(cc_limpio)

    msg.set_content(mensaje)

    # adjuntar archivos
    for archivo in archivos:

        try:

            contenido = None

            # intentar leer desde local
            if os.path.exists(archivo):

                with open(archivo, "rb") as f:
                    contenido = f.read()

            else:
                # fallback: descargar desde Blob
                print(f"⬇ Descargando archivo desde Blob: {archivo}")

                response = requests.get(archivo)

                if response.status_code == 200:
                    contenido = response.content
                else:
                    print(f"⚠ No se pudo descargar el archivo: {archivo}")
                    continue

            # limpiar nombre generado por Vercel Blob
            nombre_archivo = os.path.basename(archivo).split("-")[0] + ".pdf"

            msg.add_attachment(
                contenido,
                maintype="application",
                subtype="pdf",
                filename=nombre_archivo
            )

        except Exception as e:
            print(f"❌ Error adjuntando archivo {archivo}: {e}")

    # lista real de destinatarios (TO + CC)
    destinatarios_envio = destinatarios + cc_limpio

    print("📧 Enviando correo")
    print("Remitente:", remitente)
    print("Destinatarios:", destinatarios_envio)
    print("Adjuntos:", archivos)

    try:

        # conexión SMTP segura
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:

            smtp.starttls()
            smtp.login(remitente, password)

            smtp.send_message(
                msg,
                from_addr=remitente,
                to_addrs=destinatarios_envio
            )

        print("✅ Correo enviado correctamente")

    except Exception as e:

        print("❌ Error SMTP:", str(e))
        raise