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

    ultimos = []

    for r in registros[-5:][::-1]:

        ultimos.append({
            "fecha": r.get("fecha", ""),
            "excel": r.get("excel", ""),
            "remitente": r.get("correo", ""),  # ← AQUÍ ESTÁ LA CLAVE
            "destinatarios": r.get("destinatarios", "")
        })

    return {
        "total_circularizaciones": total_circularizaciones,
        "total_destinatarios": total_destinatarios,
        "ultimos": ultimos
    }