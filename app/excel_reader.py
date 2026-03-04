import pandas as pd

def leer_excel(ruta_excel):

    df = pd.read_excel(ruta_excel)

    destinatarios = []

    for _, fila in df.iterrows():

        nombre = fila["DESTINATARIO"]
        email = fila["EMAIL"]
        documentos = fila["DOCUMENTOS"]

        lista_documentos = [doc.strip() for doc in str(documentos).split(",")]

        destinatarios.append({
            "nombre": nombre,
            "email": email,
            "documentos": lista_documentos
        })

    return destinatarios