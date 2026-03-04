import json

USERS_FILE = "config/users.json"


def cargar_usuarios():

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def autenticar_usuario(username, password):

    usuarios = cargar_usuarios()

    if username in usuarios:

        usuario = usuarios[username]

        if usuario["password"] == password:
            return usuario

    return None