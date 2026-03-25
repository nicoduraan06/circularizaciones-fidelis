import pandas as pd
import unicodedata


def normalizar_texto(texto):
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto


def contiene_alguna_clave(valor, claves):
    valor_norm = normalizar_texto(valor)
    return any(clave in valor_norm for clave in claves)


def encontrar_fila_encabezados(df):

    posibles_destinatario = [
        "destinatario",
        "empresa",
        "cliente",
        "proveedor",
        "nombre",
        "descripcion contable"
    ]

    posibles_email = [
        "email",
        "correo",
        "correo electronico",
        "mail"
    ]

    posibles_documentos = [
        "documentos",
        "documento",
        "pdf",
        "archivo",
        "modelo de documento"
    ]

    for i in range(len(df)):

        fila = df.iloc[i].astype(str).tolist()

        tiene_email = any(
            contiene_alguna_clave(celda, posibles_email)
            for celda in fila
        )

        tiene_documentos = any(
            contiene_alguna_clave(celda, posibles_documentos)
            for celda in fila
        )

        tiene_destinatario = any(
            contiene_alguna_clave(celda, posibles_destinatario)
            for celda in fila
        )

        # obligamos a que existan email y documentos, y mejor si también destinatario
        if tiene_email and tiene_documentos:
            return i

    return None


def leer_excel(ruta_excel):

    # leer sin encabezados para detectar la fila correcta
    df_raw = pd.read_excel(ruta_excel, header=None)

    fila_header = encontrar_fila_encabezados(df_raw)

    if fila_header is None:
        raise Exception(
            "No se ha encontrado la fila de encabezados del Excel. "
            "Debe existir al menos una columna de EMAIL/CORREO y una de DOCUMENTOS/ARCHIVO."
        )

    df = pd.read_excel(ruta_excel, header=fila_header)

    # normalizar nombres de columnas
    df.columns = [str(col).strip().upper() for col in df.columns]

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
        "ARCHIVOS",
        "MODELO DE DOCUMENTO",
        "MODELO DE DOCUMENTO 1",
        "MODELO DE DOCUMENTO 2",
        "MODELO DE DOCUMENTO 3",
        "ADJUNTO",
        "ADJUNTOS"
    ]

    col_destinatario = None
    for c in columnas:
        for p in posibles_destinatario:
            if p in c:
                col_destinatario = c
                break
        if col_destinatario:
            break

    col_email = None
    for c in columnas:
        for p in posibles_email:
            if p in c:
                col_email = c
                break
        if col_email:
            break

    cols_documentos = []
    for c in columnas:
        for p in posibles_documentos:
            if p in c:
                cols_documentos.append(c)
                break

    if not col_email:
        raise Exception("No se ha encontrado ninguna columna de EMAIL en el Excel")

    if not cols_documentos:
        raise Exception("No se ha encontrado ninguna columna de DOCUMENTOS en el Excel")

    destinatarios = []

    for _, fila in df.iterrows():

        if fila.isna().all():
            continue

        nombre = ""
        if col_destinatario and not pd.isna(fila[col_destinatario]):
            nombre = str(fila[col_destinatario]).strip()

        if pd.isna(fila[col_email]):
            continue

        emails_raw = str(fila[col_email]).strip()

        if not emails_raw:
            continue

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

        documentos = list(dict.fromkeys(documentos))

        if not documentos:
            continue

        for email in emails:
            destinatarios.append({
                "nombre": nombre,
                "email": email,
                "documentos": documentos
            })

    return destinatarios