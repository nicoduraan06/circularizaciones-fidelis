import smtplib
from email.message import EmailMessage
import os


def enviar_correo(remitente, password, destinatario, asunto, mensaje, archivos):

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario
    msg.set_content(mensaje)

    # adjuntar archivos
    for archivo in archivos:

        with open(archivo, "rb") as f:
            contenido = f.read()

        nombre_archivo = os.path.basename(archivo)

        msg.add_attachment(
            contenido,
            maintype="application",
            subtype="pdf",
            filename=nombre_archivo
        )

    # conexión SMTP (Gmail)
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:

        smtp.starttls()
        smtp.login(remitente, password)
        smtp.send_message(msg)