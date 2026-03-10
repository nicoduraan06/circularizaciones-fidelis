import json
import os

# ruta absoluta compatible con Vercel
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "config", "users.json")


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