import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.mailer import enviar_correo
from services.progress_service import iniciar_progreso, incrementar_enviados, incrementar_errores
from services.error_logger_service import registrar_error

# carpeta temporal compatible con Vercel
UPLOAD_FOLDER = "/tmp/uploads"


def buscar_pdf_real(nombre_pdf):
    """
    Busca el PDF real en /tmp/uploads incluso si Vercel Blob
    le ha añadido un sufijo aleatorio.
    """

    if not os.path.exists(UPLOAD_FOLDER):
        return None

    nombre_base = nombre_pdf.replace(".pdf", "")

    for archivo in os.listdir(UPLOAD_FOLDER):

        if archivo.startswith(nombre_base) and archivo.endswith(".pdf"):
            return os.path.join(UPLOAD_FOLDER, archivo)

    return None


def descargar_pdf_desde_blob(nombre_pdf):
    """
    Si el archivo no está en /tmp, intenta descargarlo desde Blob.
    """

    try:

        # buscar la URL del blob guardada en entorno o construirla
        # aquí asumimos que los blobs están en una ruta estándar
        base_blob_url = os.getenv("BLOB_PUBLIC_URL")

        if not base_blob_url:
            return None

        url = f"{base_blob_url}/{nombre_pdf}"

        response = requests.get(url, timeout=20)

        if response.status_code == 200:

            ruta_local = os.path.join(UPLOAD_FOLDER, nombre_pdf)

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            with open(ruta_local, "wb") as f:
                f.write(response.content)

            return ruta_local

        else:
            print(f"⚠ No se pudo descargar {nombre_pdf} desde Blob")

    except Exception as e:

        print(f"❌ Error descargando {nombre_pdf}: {e}")

    return None


def enviar_un_correo(
        d,
        email_remitente,
        password,
        asunto,
        mensaje,
        cc
):

    emails = [
        e.strip()
        for e in d["email"].replace(";", ",").split(",")
        if e.strip()
    ]

    documentos = d["documentos"]

    archivos_adjuntos = []

    if isinstance(documentos, str):
        documentos = [doc.strip() for doc in documentos.split(",") if doc.strip()]

    documentos_unicos = list(set(documentos))

    for doc in documentos_unicos:

        ruta_pdf = buscar_pdf_real(doc)

        if not ruta_pdf:

            print(f"⚠ PDF no encontrado en /tmp: {doc}, intentando descargar desde Blob")

            ruta_pdf = descargar_pdf_desde_blob(doc)

        if ruta_pdf:
            archivos_adjuntos.append(ruta_pdf)
        else:
            print(f"❌ No se pudo obtener el PDF: {doc}")

    try:

        print(f"📧 Enviando correo a: {emails}")
        print(f"📎 Adjuntos encontrados: {archivos_adjuntos}")

        enviar_correo(
            email_remitente,
            password,
            emails,
            asunto,
            mensaje,
            archivos_adjuntos,
            cc
        )

        print(f"✅ Correo enviado correctamente a {emails}")

        return {"email": ", ".join(emails), "error": None}

    except Exception as e:

        print(f"❌ Error enviando a {emails}: {e}")

        registrar_error(", ".join(emails), str(e))

        return {"email": ", ".join(emails), "error": str(e)}


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

    iniciar_progreso(total)

    errores = []
    enviados_ok = []

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
                else:
                    enviados_ok.append(resultado["email"])

                incrementar_enviados()

            except Exception as e:

                print("❌ Error inesperado en worker:", e)

                errores.append("Error inesperado")
                incrementar_errores()
                incrementar_enviados()

    print("===== FIN DE LA CIRCULARIZACIÓN =====")

    asunto_resumen = "Resultado de circularización"

    lista_ok = "\n".join([f"✔ {e}" for e in enviados_ok])
    lista_error = "\n".join([f"❌ {e}" for e in errores])

    mensaje_resumen = f"""
La circularización ha finalizado correctamente.

RESULTADO DEL ENVÍO

Correos enviados correctamente:
{lista_ok if lista_ok else "Ninguno"}

Correos con error:
{lista_error if lista_error else "Ninguno"}

RESUMEN

Total destinatarios: {total}
Enviados correctamente: {len(enviados_ok)}
Errores detectados: {len(errores)}
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