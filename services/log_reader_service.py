LOG_FILE = "logs/circularizaciones.log"


def leer_historial():

    registros = []

    try:

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            contenido = f.read()

        bloques = contenido.split("=====================================")

        for bloque in bloques:

            if "Fecha:" in bloque:

                lineas = [l.strip() for l in bloque.strip().split("\n") if l.strip()]

                fecha = lineas[0].replace("Fecha:", "").strip()
                excel = lineas[1].replace("Excel:", "").strip()
                correo = lineas[2].replace("Correo:", "").strip()
                destinatarios = lineas[3].replace("Destinatarios:", "").strip()

                registros.append({
                    "fecha": fecha,
                    "excel": excel,
                    "correo": correo,
                    "destinatarios": destinatarios
                })

    except FileNotFoundError:
        pass

    return registros