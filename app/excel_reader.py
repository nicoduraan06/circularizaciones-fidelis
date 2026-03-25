import pandas as pd


def encontrar_fila_encabezados(df):

    posibles_claves = [
        "destinatario",
        "empresa",
        "cliente",
        "proveedor",
        "nombre",
        "email",
        "correo",
        "documento",
        "archivo",
        "pdf"
    ]

    for i in range(len(df)):

        fila = df.iloc[i].astype(str).str.lower().tolist()

        coincidencias = sum(
            any(clave in celda for celda in fila)
            for clave in posibles_claves
        )

        # si encuentra varias coincidencias, es header
        if coincidencias >= 2:
            return i

    return 0  # fallback


def leer_excel(ruta_excel):

    # leer sin header
    df_raw = pd.read_excel(ruta_excel, header=None)

    # detectar fila header real
    fila_header = encontrar_fila_encabezados(df_raw)

    # volver a leer con header correcto
    df = pd.read_excel(ruta_excel, header=fila_header)

    # Normalizar columnas
    df.columns = df.columns.astype(str).str.strip().str.upper()

    columnas = list(df.columns)

    posibles_destinatario = [
        "DESTINATARIO",
        "EMPRESA",
        "CLIENTE",
        "PROVEEDOR",
        "NOMBRE",
        "DESCRIPCIÓN CONTABLE",
        "DESCRIPCION CONTABLE"
    ]

    posibles_email = [
        "EMAIL",
        "EMAIL*",
        "CORREO",
        "CORREO ELECTRONICO",
        "CORREO ELECTRÓNICO",
        "MAIL"
    ]

    posibles_documentos = [
        "DOCUMENTOS",
        "DOCUMENTO",
        "PDF",
        "ARCHIVO",
        "MODELO DE DOCUMENTO",
        "MODELO DE DOCUMENTO 1",
        "MODELO DE DOCUMENTO 2",
        "MODELO DE DOCUMENTO 3"
    ]

    # detectar columna destinatario
    col_destinatario = None
    for c in columnas:
        for p in posibles_destinatario:
            if p in c:
                col_destinatario = c
                break
        if col_destinatario:
            break

    # detectar columna email
    col_email = None
    for c in columnas:
        for p in posibles_email:
            if p in c:
                col_email = c
                break
        if col_email:
            break

    # detectar columnas de documentos
    cols_documentos = []
    for c in columnas:
        for p in posibles_documentos:
            if p in c:
                cols_documentos.append(c)

    if not col_email:
        raise Exception("No se ha encontrado ninguna columna de EMAIL en el Excel")

    if not cols_documentos:
        raise Exception("No se ha encontrado ninguna columna de DOCUMENTOS en el Excel")

    destinatarios = []

    for _, fila in df.iterrows():

        # ignorar filas completamente vacías
        if fila.isna().all():
            continue

        nombre = ""
        if col_destinatario and not pd.isna(fila[col_destinatario]):
            nombre = str(fila[col_destinatario]).strip()

        emails_raw = str(fila[col_email])

        # separar múltiples emails
        emails = [
            e.strip()
            for e in emails_raw.replace(";", ",").split(",")
            if e.strip()
        ]

        documentos = []

        for col in cols_documentos:

            valor = fila[col]

            if pd.isna(valor):
                continue

            docs = str(valor).split(",")

            for d in docs:
                d = d.strip()
                if d:
                    documentos.append(d)

        # eliminar duplicados
        documentos = list(set(documentos))

        for email in emails:

            destinatarios.append({
                "nombre": nombre,
                "email": email,
                "documentos": documentos
            })

    return destinatarios