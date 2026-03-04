import json

USERS_FILE = "config/users.json"


def obtener_usuarios():

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def guardar_usuarios(usuarios):

    with open(USERS_FILE, "w", encoding="utf-8") as f:
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