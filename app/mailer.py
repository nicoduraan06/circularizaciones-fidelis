import smtplib
from email.message import EmailMessage
import os
import requests
import urllib.parse
import mimetypes


def enviar_correo(remitente, password, destinatario, asunto, mensaje, archivos, cc=None):

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente

    if isinstance(destinatario, str):
        destinatarios = [d.strip() for d in destinatario.split(",") if d.strip()]
    else:
        destinatarios = destinatario

    msg["To"] = ", ".join(destinatarios)

    cc_limpio = []
    if cc:
        if isinstance(cc, str):
            cc_limpio = [c.strip() for c in cc.split(",") if c.strip()]
        else:
            cc_limpio = cc
        msg["Cc"] = ", ".join(cc_limpio)

    msg.set_content(mensaje)

    for archivo in archivos:

        try:

            if isinstance(archivo, tuple):
                ruta_archivo, nombre_original = archivo
            else:
                ruta_archivo = archivo
                nombre_original = os.path.basename(archivo)

            contenido = None

            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, "rb") as f:
                    contenido = f.read()
            else:
                print(f"⬇ Descargando archivo desde Blob: {ruta_archivo}")

                response = requests.get(ruta_archivo)

                if response.status_code == 200:
                    contenido = response.content
                else:
                    print(f"⚠ No se pudo descargar el archivo: {ruta_archivo}")
                    continue

            nombre_archivo = urllib.parse.unquote(nombre_original)

            tipo, _ = mimetypes.guess_type(nombre_archivo)

            if tipo and "/" in tipo:
                maintype, subtype = tipo.split("/", 1)
            else:
                maintype, subtype = "application", "octet-stream"

            msg.add_attachment(
                contenido,
                maintype=maintype,
                subtype=subtype,
                filename=nombre_archivo
            )

        except Exception as e:
            print(f"❌ Error adjuntando archivo {archivo}: {e}")

    destinatarios_envio = destinatarios + cc_limpio

    print("📧 Enviando correo")
    print("Remitente:", remitente)
    print("Destinatarios:", destinatarios_envio)
    print("Adjuntos:", archivos)

    try:
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