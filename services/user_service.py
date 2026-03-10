import json
import os

# ruta del archivo en el proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "config", "users.json")

# copia editable en Vercel
TMP_USERS_FILE = "/tmp/users.json"


def obtener_usuarios():

    # si existe versión temporal (Vercel) usarla
    if os.path.exists(TMP_USERS_FILE):
        archivo = TMP_USERS_FILE
    else:
        archivo = USERS_FILE

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def guardar_usuarios(usuarios):

    # en Vercel guardamos en /tmp
    with open(TMP_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4)


def crear_usuario(username, password, email):

    usuarios = obtener_usuarios()

    usuarios[username] = {
        "password": password,
        "email": email
    }

    guardar_usuarios(usuarios)


def eliminar_usuario(username):

    usuarios = obtener_usuarios()

    if username in usuarios:
        del usuarios[username]

    guardar_usuarios(usuarios)