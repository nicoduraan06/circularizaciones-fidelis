USUARIOS = {
    "nicolas": {
        "password": "1234",
        "email": "nicolasdu2006@gmail.com"
    }
}


def autenticar_usuario(username, password):

    usuario = USUARIOS.get(username)

    if not usuario:
        return None

    if usuario["password"] != password:
        return None

    return usuario