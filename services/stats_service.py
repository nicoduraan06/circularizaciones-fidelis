from services.log_reader_service import leer_historial


def obtener_estadisticas():

    registros = leer_historial()

    total_circularizaciones = len(registros)

    total_destinatarios = 0

    for r in registros:
        try:
            total_destinatarios += int(r["destinatarios"])
        except:
            pass

    ultimos = registros[-5:][::-1]

    return {
        "total_circularizaciones": total_circularizaciones,
        "total_destinatarios": total_destinatarios,
        "ultimos": ultimos
    }