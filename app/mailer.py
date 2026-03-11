import smtplib
from email.message import EmailMessage
import os


def enviar_correo(remitente, password, destinatario, asunto, mensaje, archivos, cc=None):

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    # añadir CC si existen
    if cc:
        msg["Cc"] = ", ".join(cc)

    msg.set_content(mensaje)

    # adjuntar archivos
    for archivo in archivos:

        if not os.path.exists(archivo):
            print(f"⚠ Archivo no encontrado: {archivo}")
            continue

        with open(archivo, "rb") as f:
            contenido = f.read()

        nombre_archivo = os.path.basename(archivo)

        msg.add_attachment(
            contenido,
            maintype="application",
            subtype="pdf",
            filename=nombre_archivo
        )

    # lista real de destinatarios (TO + CC)
    destinatarios_envio = [destinatario]

    if cc:
        destinatarios_envio += cc

    # conexión SMTP segura
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:

        smtp.starttls()
        smtp.login(remitente, password)
        smtp.send_message(msg, to_addrs=destinatarios_envio)